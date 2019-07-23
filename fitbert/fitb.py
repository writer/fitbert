import operator
from collections import defaultdict
from functools import reduce
from typing import Dict, List, Tuple, Union, overload

import torch
from fitbert.delemmatize import Delemmatizer
from fitbert.utils import mask as _mask
from pytorch_pretrained_bert import BertForMaskedLM, tokenization


class FitBert:
    def __init__(
        self,
        model=None,
        tokenizer=None,
        model_name="bert-large-uncased",
        mask_token="***mask***",
    ):
        self.mask_token = mask_token
        self.delemmatizer = Delemmatizer()
        print("using model:", model_name)
        if not model:
            self.bert = BertForMaskedLM.from_pretrained(model_name)
        else:
            self.bert = model
        if not tokenizer:
            self.tokenizer = tokenization.BertTokenizer.from_pretrained(model_name)
        else:
            self.tokenizer = tokenizer
        self.bert.eval()

    @staticmethod
    def softmax(x):
        return x.exp() / (x.exp().sum(-1)).unsqueeze(-1)

    @staticmethod
    def is_multi_word(options: List[str]) -> bool:
        return True in [len(option.split()) > 1 for option in options]

    def mask(self, s: str, span: Tuple[int, int]) -> Tuple[str, str]:
        return _mask(s, span, mask_token=self.mask_token)

    def _get_probs_for_words(self, sent: str, words: List[str]):
        """
        idea from (don't worry, it's Apache2 licensed)
        https://github.com/yoavg/bert-syntax/blob/master/eval_bert.py
        but modified for list of words

        also useful,
        https://stackoverflow.com/questions/54978443/predicting-missing-words-in-a-sentence-natural-language-processing-model

        @TODO this is not optimized! It loops instead of batching, forgive me, Tensor Gods!
        """
        option_2_token_count: Dict[str, int] = defaultdict(int)
        for word in words:
            toks = self.tokenizer.tokenize(word)
            option_2_token_count[word] += len(toks)

        token_count_2_option: Dict[int, List[str]] = defaultdict(list)
        for k, v in option_2_token_count.items():
            token_count_2_option[v].append(k)

        final_scores: Dict[str, List[float]] = {}
        for tok_len, options_of_given_length in token_count_2_option.items():

            pre, target_s, post = sent.split("***")
            if "mask" in target_s.lower():
                target = ["[MASK]"] * tok_len
            else:
                # not sure how to get here, but it was in the original
                target = self.tokenizer.tokenize(target_s)

            tokens = ["[CLS]"] + self.tokenizer.tokenize(pre)
            target_idx = len(tokens)
            tokens += target + self.tokenizer.tokenize(post) + ["[SEP]"]
            input_ids = self.tokenizer.convert_tokens_to_ids(tokens)
            for option in options_of_given_length:
                try:
                    toks = self.tokenizer.tokenize(option)
                    tok_ids = self.tokenizer.convert_tokens_to_ids(toks)
                except KeyError:
                    print("couldn't convert tokens to IDs, ", toks)
                    return None
                tens = torch.LongTensor(input_ids).unsqueeze(0)

                # don't need gradients at inference time, thank god
                # speeds things up considerably
                with torch.no_grad():
                    pred = self.bert(tens)
                scores = []
                for i in range(tok_len):
                    res = pred[0, target_idx + i]
                    prob = self.softmax(res)
                    score = float(prob[tok_ids[i]].item())
                    # to explain the res[tok_ids] syntax:
                    # >>> a = torch.tensor([1.0, 1.1, 1.2, 1.3])
                    # >>> a[[1,2]]
                    # tensor([1.1000, 1.2000])
                    scores.append(score)
                final_scores[option] = reduce(operator.mul, scores, 1)
        return final_scores

    def _delemmatize_options(self, options: List[str]) -> List[str]:
        for word in options:
            words_with_shared_lemma = self.delemmatizer(word)
            for w in words_with_shared_lemma:
                if w not in options:
                    options.append(w)
        return options

    def rank(
        self, sent: str, options: List[str], delemmatize: bool = False
    ) -> List[str]:
        if len(options) == 1:
            delemmatize = True
        if delemmatize:
            options = self._delemmatize_options(options)
        scored = self._get_probs_for_words(sent, options)
        ranked = sorted(scored.items(), key=lambda x: x[1], reverse=True)
        return list(list(zip(*ranked))[0])

    def fitb(self, sent: str, options: List[str], delemmatize: bool = False) -> str:
        ranked = self.rank(sent, options, delemmatize)
        best_word = ranked[0]
        return sent.replace(self.mask_token, best_word)

    def mask_fitb(self, sent: str, span: Tuple[int, int]) -> str:
        masked_str, replaced = self.mask(sent, span)
        options = [replaced]
        return self.fitb(masked_str, options, delemmatize=True)

    def get_sentence_options(self, sent: str, options: List[str]) -> List[str]:
        sentence_options = []
        for option in options:
            sentence_option = sent.replace(self.mask_token, option)
            sentence_options.append(sentence_option)
        return sentence_options

    def get_sentence_score(self, sent: str) -> float:
        sentence_prob = []
        words = sent.split()
        # remove and rememebr the ending sign
        end_sign = words[-1][-1]
        words[-1] = words[-1][:-1]
        for i, word in enumerate(words):
            masked_words = words[:]
            masked_words[i] = self.mask_token
            masked_sentence = " ".join(masked_words) + end_sign
            prob_dict = self._get_probs_for_words(masked_sentence, [word])
            sentence_prob.append(prob_dict[word])
        return reduce(operator.mul, sentence_prob, 1)

    def sentence_prob_to_rank(self, sent: str, options: List[str]) -> List[str]:
        sentence_options = self.get_sentence_options(sent, options)
        opt_probs = []
        for option, sentence_option in zip(options, sentence_options):
            sentence_prob = self.get_sentence_score(sentence_option)
            opt_probs.append([option, sentence_prob])
        opt_probs = sorted(opt_probs, key=lambda x: x[1], reverse=True)
        ranked = [e[0] for e in opt_probs]
        return ranked

    def simplify_options(self, sent: str, options: List[str]):
        min_option_len = min([len(o.split()) for o in options])
        last_word = ""
        first_word = ""
        if min_option_len > 1:
            # check if last or first common:
            if len(set([o.split()[-1] for o in options])) == 1:
                last_word = options[0].split()[-1]
                options = [" ".join(o.split()[:-1]) for o in options]
                sent = sent.replace(self.mask_token, " ".join([self.mask_token, last_word]))
            elif len(set([o.split()[0] for o in options])) == 1:
                first_word = options[0].split()[0]
                options = [" ".join(o.split()[1:]) for o in options]
                sent = sent.replace(self.mask_token, " ".join([first_word, self.mask_token]))
        return options, sent, first_word, last_word

    def rank_multi(self, sent: str, options: List[str]) -> List[str]:
        ranked_options = []
        if self.is_multi_word(options):
            options, sent, first_word, last_word = self.simplify_options(sent, options)
            ranked_options = self.sentence_prob_to_rank(sent, options)
            ranked_options = [" ".join([first_word, r, last_word]).strip() for r in ranked_options]
        else:
            ranked_options = self.rank(sent, options=options)
        return ranked_options
