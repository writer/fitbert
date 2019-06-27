"""
This is copied from the prototype in passive voice
"""

from typing import Dict, List

import numpy as np
import torch
from pytorch_pretrained_bert import BertForMaskedLM, tokenization
from qai import Cleantext, make_issue
from word_forms.word_forms import get_word_forms


def get_all_tenses(verb) -> List[str]:
    """
    verb is a spacy token
    get_word_forms(verb.lemma_)['v'] is a possibly empty set
    """
    literal = verb.text
    unique_tokens = get_word_forms(verb.lemma_)["v"]
    if literal not in unique_tokens:
        unique_tokens.add(literal)
    return list(unique_tokens)


model_name = "bert-large-uncased"
print("using model:", model_name)
bert = BertForMaskedLM.from_pretrained(model_name)
tokenizer = tokenization.BertTokenizer.from_pretrained(model_name)
bert.eval()


def get_probs_for_words(sent: str, words: List[str]):
    """
    Thanks, Yoav (don't worry, it's Apache2 licensed)
    idea from
    https://github.com/yoavg/bert-syntax/blob/master/eval_bert.py
    but modified for list of words
    """
    pre, target, post = sent.split("***")
    if "mask" in target.lower():
        target = ["[MASK]"]
    else:
        target = tokenizer.tokenize(target)
    tokens = ["[CLS]"] + tokenizer.tokenize(pre)
    target_idx = len(tokens)
    tokens += target + tokenizer.tokenize(post) + ["[SEP]"]
    input_ids = tokenizer.convert_tokens_to_ids(tokens)
    try:
        word_ids = tokenizer.convert_tokens_to_ids(words)
    except KeyError:
        print("couldn't convert tokens to IDs, ", words)
        return None
    tens = torch.LongTensor(input_ids).unsqueeze(0)
    res = bert(tens)[0, target_idx]
    scores = res[word_ids]
    return [float(x) for x in scores]


def bert_likely_word(sent, words):
    # print("Hi from BERT, getting scores")
    scores = get_probs_for_words(sent, words)
    # print("getting best word")
    best_word = words[np.argmax(scores)]
    # print("bert_likely_word: ", best_word)
    return sent.replace("***mask***", best_word).capitalize()


class Analyzer(object):
    obj2sub = {"them": "they", "me": "I", "her": "she", "him": "he", "us": "we"}

    def __init__(self):
        """
        this is how to pass spacy extensions to qai
        equivalent to
        from spacy.tokens import Token
        Token.set_extension("mask", default=False)
        etc
        """
        spacy_extensions = {
            "Tokens": [
                {"name": "mask", "kwargs": {"default": False}},
                {"name": "is_used", "kwargs": {"default": False}},
            ]
        }
        self.cleaner = Cleantext(use_spacy=True, spacy_extensions=spacy_extensions)

    def simple_activator(self, doc):
        """ this should be a class """

        root = ""
        for token in doc:
            if token.dep_ == "ROOT":
                verbs = get_all_tenses(token)
                root = token.text

        def get_true_subject(doc, default="SUBJECT"):
            for chunk in doc.noun_chunks:
                if chunk.root.head.text == "by":
                    sub = chunk.text
                    if sub in self.obj2sub.keys():
                        sub = self.obj2sub[sub]
                    return sub
            return default

        def get_object_strings(doc):
            obs = []
            for chunk in doc.noun_chunks:
                for token in chunk.subtree:
                    # this is
                    token._.is_used = True
                if chunk.root.head.text == "by":
                    pass
                elif chunk.root.head.text == root:
                    obs.insert(0, chunk.text)
                else:
                    obs.append(chunk.root.head.text + " " + chunk.text)
            return obs

        def get_the_rest(doc):
            rest = ""
            for token in doc:
                if not token._.is_used:
                    rest += f" {token.text}"
            return rest

        def sentence_builder(doc):
            mask = "***mask***"
            return "{subject} {mask} {object}{rest}".format(
                subject=get_true_subject(doc),
                mask=mask,
                object=" ".join(get_object_strings(doc)),
                rest=get_the_rest(doc),
            )

        masked_sent = sentence_builder(doc)
        sent = bert_likely_word(masked_sent, verbs)
        return sent

    def activate(self, doc):
        is_simple, is_explicit_subject = False, False
        for token in doc:
            if token.dep_ in ["nsubjpass"]:
                is_simple = True
            elif token.dep_ in ["agent"]:
                is_explicit_subject = True

        if is_simple and is_explicit_subject:
            return [self.simple_activator(doc)]
        return []

    def is_passive_token(self, token) -> bool:
        return str(token.dep_) in ["auxpass", "csubjpass", "nsubjpass"]

    def analyze(self, phrase: str) -> List[Dict]:
        sentences = self.cleaner.segment_sentences(phrase)
        issues: List = []
        for sent in sentences:
            passive = False
            for token in sent:
                if self.is_passive_token(token):
                    passive = True
            if passive:
                doc, sent = sent, str(sent)
                start = phrase.find(sent)
                end = start + len(sent)
                issue = make_issue(
                    sent,
                    start,
                    end,
                    issue_type="passive-voice",
                    score=0,
                    description="This sentence is in the passive voice.",
                    suggestions=self.activate(doc),
                )
                issues.append(issue)
        return issues
