from collections import defaultdict
from typing import Dict, List, Tuple, Union, overload

import torch
from pytorch_pretrained_bert import BertForMaskedLM, tokenization

from fitbert.delemmatize import Delemmatizer
from fitbert.utils import mask as _mask


class FitBert:
    mask_token = "***mask***"

    def __init__(self, model=None, tokenizer=None, model_name="bert-large-uncased"):
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
    def mask(s: str, span: Tuple[int, int]) -> Tuple[str, str]:
        return _mask(s, span, mask_token=FitBert.mask_token)

    def _get_probs_for_words(self, sent: str, words: List[str], agg=max):
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
                    # to explain the res[tok_ids] syntax:
                    # >>> a = torch.tensor([1.0, 1.1, 1.2, 1.3])
                    # >>> a[[1,2]]
                    # tensor([1.1000, 1.2000])
                    score = float(res[tok_ids[i]].item())
                    scores.append(score)
                # should we sum scores? max? pool? something else?
                # currently defaulting to max
                final_scores[option] = agg(scores)
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
        return sent.replace("***mask***", best_word)

    def mask_fitb(self, sent: str, span: Tuple[int, int]) -> str:
        masked_str, replaced = self.mask(sent, span)
        options = [replaced]
        return self.fitb(masked_str, options, delemmatize=True)

