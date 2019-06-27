from typing import Dict, List, Tuple

import torch
from pytorch_pretrained_bert import BertForMaskedLM, tokenization

from fitbert.delemmatize import Delemmatizer
from fitbert.utils import sort_first_by_second


class FitBert:
    def __init__(self, model=None, tokenizer=None, model_name="bert-large-uncased"):
        self.mask_token = "***mask***"
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

    def _get_probs_for_words(self, sent: str, words: List[str]):
        """
        Thanks, Yoav (don't worry, it's Apache2 licensed)
        idea from
        https://github.com/yoavg/bert-syntax/blob/master/eval_bert.py
        but modified for list of words

        PLAN
        THIS ONLY WORKS IF ALL WORDS ARE ONE BERT TOKEN
        NEED TO FIX
        """
        pre, target, post = sent.split("***")
        if "mask" in target.lower():
            target = ["[MASK]"]
        else:
            target = self.tokenizer.tokenize(target)
        tokens = ["[CLS]"] + self.tokenizer.tokenize(pre)
        target_idx = len(tokens)
        tokens += target + self.tokenizer.tokenize(post) + ["[SEP]"]
        input_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        try:
            # this line only works if a word == one token
            word_ids = self.tokenizer.convert_tokens_to_ids(words)
        except KeyError:
            print("couldn't convert tokens to IDs, ", words)
            return None
        tens = torch.LongTensor(input_ids).unsqueeze(0)
        res = self.bert(tens)[0, target_idx]
        scores = res[word_ids]
        return [float(x) for x in scores]

    def _delemmatize_options(self, options: List[str]) -> List[str]:
        for word in options:
            words_with_shared_lemma = self.delemmatizer(word)
            for w in words_with_shared_lemma:
                if w not in options:
                    options.append(w)
        return options

    def mask(self, s: str, span: Tuple[int, int]) -> Tuple[str, str]:
        subs = s[span[0] : span[1]]
        return s.replace(subs, self.mask_token), subs

    def rank(
        self, sent: str, options: List[str], delemmatize: bool = False
    ) -> List[str]:
        if len(options) == 1:
            delemmatize = True
        if delemmatize:
            options = self._delemmatize_options(options)
        scores = self._get_probs_for_words(sent, options)
        ranked = sort_first_by_second(options, scores)
        return ranked

    def fitb(self, sent: str, options: List[str], delemmatize: bool = False) -> str:
        ranked = self.rank(sent, options, delemmatize)
        best_word = ranked[0]
        return sent.replace("***mask***", best_word)

    def mask_fitb(self, sent: str, span: Tuple[int, int]) -> str:
        masked_str, replaced = self.mask(sent, span)
        options = [replaced]
        return self.fitb(masked_str, options, delemmatize=True)

