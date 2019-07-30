import re
from pprint import pprint

import nltk as nltk
import pyinflect
import spacy
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer

nlp = spacy.load("en_core_web_sm")
porter = PorterStemmer()


def conjugate(verb_token):

    verb_forms = []

    VB = verb_token._.inflect("VB")
    if not VB is None:
        VBP = verb_token._.inflect("VBP")
        VBZ = verb_token._.inflect("VBZ")
        VBG = verb_token._.inflect("VBG")
        VBD = verb_token._.inflect("VBD")
        VBN = verb_token._.inflect("VBN")

        if verb_token.lemma_ == "be":
            verb_forms += [
                {
                    "1P": False,
                    "1S": True,
                    "2P": False,
                    "2S": False,
                    "3P": False,
                    "3S": False,
                    "aux_1": "",
                    "aux_2": "",
                    "is_active": True,
                    "tense": "present",
                    "tense_name": "present simple",
                    "verb": VBP,
                },
                {
                    "1P": True,
                    "1S": False,
                    "2P": True,
                    "2S": True,
                    "3P": True,
                    "3S": False,
                    "aux_1": "",
                    "aux_2": "",
                    "is_active": True,
                    "tense": "present",
                    "tense_name": "present simple",
                    "verb": "are",
                },
            ]
        else:
            verb_forms += [
                {
                    "1P": True,
                    "1S": True,
                    "2P": True,
                    "2S": True,
                    "3P": True,
                    "3S": False,
                    "aux_1": "",
                    "aux_2": "",
                    "is_active": True,
                    "tense": "present",
                    "tense_name": "present simple",
                    "verb": VBP,
                }
            ]

        verb_forms += [
            {
                "1P": False,
                "1S": False,
                "2P": False,
                "2S": False,
                "3P": False,
                "3S": True,
                "aux_1": "",
                "aux_2": "",
                "is_active": True,
                "tense": "present",
                "tense_name": "present simple",
                "verb": VBZ,
            },
            {
                "1P": False,
                "1S": True,
                "2P": False,
                "2S": False,
                "3P": False,
                "3S": False,
                "aux_1": "am",
                "aux_2": "",
                "is_active": False,
                "tense": "present",
                "tense_name": "present simple",
                "verb": VBN,
            },
            {
                "1P": False,
                "1S": False,
                "2P": False,
                "2S": False,
                "3P": False,
                "3S": True,
                "aux_1": "is",
                "aux_2": "",
                "is_active": False,
                "tense": "present",
                "tense_name": "present simple",
                "verb": VBN,
            },
            {
                "1P": True,
                "1S": False,
                "2P": True,
                "2S": True,
                "3P": True,
                "3S": False,
                "aux_1": "are",
                "aux_2": "",
                "is_active": False,
                "tense": "present",
                "tense_name": "present simple",
                "verb": VBN,
            },
            {
                "1P": False,
                "1S": True,
                "2P": False,
                "2S": False,
                "3P": False,
                "3S": False,
                "aux_1": "am",
                "aux_2": "",
                "is_active": True,
                "tense": "present",
                "tense_name": "present continuous",
                "verb": VBG,
            },
            {
                "1P": False,
                "1S": False,
                "2P": False,
                "2S": False,
                "3P": False,
                "3S": True,
                "aux_1": "is",
                "aux_2": "",
                "is_active": True,
                "tense": "present",
                "tense_name": "present continuous",
                "verb": VBG,
            },
            {
                "1P": True,
                "1S": False,
                "2P": True,
                "2S": True,
                "3P": True,
                "3S": False,
                "aux_1": "are",
                "aux_2": "",
                "is_active": True,
                "tense": "present",
                "tense_name": "present continuous",
                "verb": VBG,
            },
            {
                "1P": False,
                "1S": True,
                "2P": False,
                "2S": False,
                "3P": False,
                "3S": False,
                "aux_1": "am",
                "aux_2": "being",
                "is_active": False,
                "tense": "present",
                "tense_name": "present continuous",
                "verb": VBN,
            },
            {
                "1P": False,
                "1S": False,
                "2P": False,
                "2S": False,
                "3P": False,
                "3S": True,
                "aux_1": "is",
                "aux_2": "being",
                "is_active": False,
                "tense": "present",
                "tense_name": "present continuous",
                "verb": VBN,
            },
            {
                "1P": True,
                "1S": False,
                "2P": True,
                "2S": True,
                "3P": True,
                "3S": False,
                "aux_1": "are",
                "aux_2": "being",
                "is_active": False,
                "tense": "present",
                "tense_name": "present continuous",
                "verb": VBN,
            },
            {
                "1P": True,
                "1S": True,
                "2P": True,
                "2S": True,
                "3P": True,
                "3S": True,
                "aux_1": "",
                "aux_2": "",
                "is_active": True,
                "tense": "past",
                "tense_name": "past simple",
                "verb": VBD,
            },
            {
                "1P": False,
                "1S": True,
                "2P": False,
                "2S": False,
                "3P": False,
                "3S": True,
                "aux_1": "was",
                "aux_2": "",
                "is_active": False,
                "tense": "past",
                "tense_name": "past simple",
                "verb": VBN,
            },
            {
                "1P": True,
                "1S": False,
                "2P": True,
                "2S": True,
                "3P": True,
                "3S": False,
                "aux_1": "were",
                "aux_2": "",
                "is_active": False,
                "tense": "past",
                "tense_name": "past simple",
                "verb": VBN,
            },
            {
                "1P": False,
                "1S": True,
                "2P": False,
                "2S": False,
                "3P": False,
                "3S": True,
                "aux_1": "was",
                "aux_2": "",
                "is_active": True,
                "tense": "past",
                "tense_name": "past continuous",
                "verb": VBG,
            },
            {
                "1P": True,
                "1S": False,
                "2P": True,
                "2S": True,
                "3P": True,
                "3S": False,
                "aux_1": "were",
                "aux_2": "",
                "is_active": True,
                "tense": "past",
                "tense_name": "past continuous",
                "verb": VBG,
            },
            {
                "1P": False,
                "1S": True,
                "2P": False,
                "2S": False,
                "3P": False,
                "3S": True,
                "aux_1": "was",
                "aux_2": "being",
                "is_active": False,
                "tense": "past",
                "tense_name": "past continuous",
                "verb": VBN,
            },
            {
                "1P": True,
                "1S": False,
                "2P": True,
                "2S": True,
                "3P": True,
                "3S": False,
                "aux_1": "were",
                "aux_2": "being",
                "is_active": False,
                "tense": "past",
                "tense_name": "past continuous",
                "verb": VBN,
            },
            {
                "1P": True,
                "1S": True,
                "2P": True,
                "2S": True,
                "3P": True,
                "3S": False,
                "aux_1": "have",
                "aux_2": "",
                "is_active": True,
                "tense": "present",
                "tense_name": "present perfect simple",
                "verb": VBN,
            },
            {
                "1P": False,
                "1S": False,
                "2P": False,
                "2S": False,
                "3P": False,
                "3S": True,
                "aux_1": "has",
                "aux_2": "",
                "is_active": True,
                "tense": "present",
                "tense_name": "present perfect simple",
                "verb": VBN,
            },
            {
                "1P": True,
                "1S": True,
                "2P": True,
                "2S": True,
                "3P": True,
                "3S": False,
                "aux_1": "have",
                "aux_2": "been",
                "is_active": False,
                "tense": "present",
                "tense_name": "present perfect simple",
                "verb": VBN,
            },
            {
                "1P": False,
                "1S": False,
                "2P": False,
                "2S": False,
                "3P": False,
                "3S": True,
                "aux_1": "has",
                "aux_2": "been",
                "is_active": False,
                "tense": "present",
                "tense_name": "present perfect simple",
                "verb": VBN,
            },
            {
                "1P": True,
                "1S": True,
                "2P": True,
                "2S": True,
                "3P": True,
                "3S": False,
                "aux_1": "have",
                "aux_2": "been",
                "is_active": True,
                "tense": "present",
                "tense_name": "present perfect continuous",
                "verb": VBG,
            },
            {
                "1P": False,
                "1S": False,
                "2P": False,
                "2S": False,
                "3P": False,
                "3S": True,
                "aux_1": "has",
                "aux_2": "been",
                "is_active": True,
                "tense": "present",
                "tense_name": "present perfect continuous",
                "verb": VBG,
            },
            {
                "1P": True,
                "1S": True,
                "2P": True,
                "2S": True,
                "3P": True,
                "3S": False,
                "aux_1": "have",
                "aux_2": "been being",
                "is_active": False,
                "tense": "present",
                "tense_name": "present perfect continuous",
                "verb": VBN,
            },
            {
                "1P": False,
                "1S": False,
                "2P": False,
                "2S": False,
                "3P": False,
                "3S": True,
                "aux_1": "has",
                "aux_2": "been being",
                "is_active": False,
                "tense": "present",
                "tense_name": "present perfect continuous",
                "verb": VBN,
            },
            {
                "1P": True,
                "1S": True,
                "2P": True,
                "2S": True,
                "3P": True,
                "3S": True,
                "aux_1": "had",
                "aux_2": "",
                "is_active": True,
                "tense": "past",
                "tense_name": "past perfect simple",
                "verb": VBN,
            },
            {
                "1P": True,
                "1S": True,
                "2P": True,
                "2S": True,
                "3P": True,
                "3S": True,
                "aux_1": "had",
                "aux_2": "been",
                "is_active": False,
                "tense": "past",
                "tense_name": "past perfect simple",
                "verb": VBN,
            },
            {
                "1P": True,
                "1S": True,
                "2P": True,
                "2S": True,
                "3P": True,
                "3S": True,
                "aux_1": "had",
                "aux_2": "been",
                "is_active": True,
                "tense": "past",
                "tense_name": "past perfect continuous",
                "verb": VBG,
            },
            {
                "1P": True,
                "1S": True,
                "2P": True,
                "2S": True,
                "3P": True,
                "3S": True,
                "aux_1": "had",
                "aux_2": "been",
                "is_active": False,
                "tense": "past",
                "tense_name": "past perfect continuous",
                "verb": VBN,
            },
            {
                "1P": True,
                "1S": True,
                "2P": True,
                "2S": True,
                "3P": True,
                "3S": True,
                "aux_1": "will",
                "aux_2": "",
                "is_active": True,
                "tense": "future",
                "tense_name": "future simple",
                "verb": VB,
            },
            {
                "1P": True,
                "1S": True,
                "2P": True,
                "2S": True,
                "3P": True,
                "3S": True,
                "aux_1": "will",
                "aux_2": "be",
                "is_active": False,
                "tense": "future",
                "tense_name": "future simple",
                "verb": VBN,
            },
            {
                "1P": True,
                "1S": True,
                "2P": True,
                "2S": True,
                "3P": True,
                "3S": True,
                "aux_1": "will",
                "aux_2": "be",
                "is_active": True,
                "tense": "future",
                "tense_name": "future continuous",
                "verb": VBG,
            },
            {
                "1P": True,
                "1S": True,
                "2P": True,
                "2S": True,
                "3P": True,
                "3S": True,
                "aux_1": "will",
                "aux_2": "be being",
                "is_active": False,
                "tense": "future",
                "tense_name": "future continuous",
                "verb": VBN,
            },
            {
                "1P": True,
                "1S": True,
                "2P": True,
                "2S": True,
                "3P": True,
                "3S": True,
                "aux_1": "will",
                "aux_2": "have",
                "is_active": True,
                "tense": "future",
                "tense_name": "future perfect simple",
                "verb": VBN,
            },
            {
                "1P": True,
                "1S": True,
                "2P": True,
                "2S": True,
                "3P": True,
                "3S": True,
                "aux_1": "will",
                "aux_2": "have been",
                "is_active": False,
                "tense": "future",
                "tense_name": "future perfect simple",
                "verb": VBN,
            },
            {
                "1P": True,
                "1S": True,
                "2P": True,
                "2S": True,
                "3P": True,
                "3S": True,
                "aux_1": "will",
                "aux_2": "have been",
                "is_active": True,
                "tense": "future",
                "tense_name": "future perfect continuous",
                "verb": VBG,
            },
            {
                "1P": True,
                "1S": True,
                "2P": True,
                "2S": True,
                "3P": True,
                "3S": True,
                "aux_1": "will",
                "aux_2": "have been being",
                "is_active": False,
                "tense": "future",
                "tense_name": "future perfect continuous",
                "verb": VBN,
            },
        ]

    return verb_forms


adv_order_exceptions = [
    "there",
    "here",
    "everywhere",
    "elsewhere",
    "anywhere",
    "nowhere",
    "somewhere",
]


def get_verb_options(
    verb, verb_phrase_inffix="", tense=["present", "past", "future"], is_active=True
):
    verb_forms = conjugate(verb)
    verb_forms = filter(
        lambda x: x["is_active"] == is_active and x["tense"] in tense, verb_forms
    )
    options = []
    for verb_form in verb_forms:
        if verb_phrase_inffix.lower() in adv_order_exceptions:
            elements = [
                verb_phrase_inffix,
                verb_form["aux_1"],
                verb_form["aux_2"],
                verb_form["verb"],
            ]
        else:
            elements = [
                verb_form["aux_1"],
                verb_phrase_inffix,
                verb_form["aux_2"],
                verb_form["verb"],
            ]
        verb_phrase = re.sub(r"\s{2,}", " ", " ".join(elements)).strip()
        options.append(verb_phrase)
    return options


def get_related_options(word, if_strict=True):
    synsets = wn.synsets(word)
    if not synsets:
        return []

    lemmas = []
    for s in synsets:
        for l in s.lemmas():
            lemmas += [l]
    derivationally_related_forms = [
        (l, l.derivationally_related_forms()) for l in lemmas
    ]
    related_noun_lemmas = []

    for drf in derivationally_related_forms:
        for l in drf[1]:
            related_noun_lemmas += [l]

    words = [l.name() for l in related_noun_lemmas]
    len_words = len(words)

    related_forms = [(w, float(words.count(w)) / len_words) for w in set(words)]
    related_forms.sort(key=lambda w: -w[1])

    related_forms = [x[0] for x in related_forms]
    related_forms = list(set(related_forms))

    if if_strict:
        word_stem = porter.stem(word)
        related_forms = [r for r in related_forms if porter.stem(r) == word_stem]
    return related_forms


if __name__ == "__main__":

    verb_token = nlp("direct")[0]

    verb_forms = conjugate(verb_token)
    related_words = get_related_options("direct", True)
    verb_options = get_verb_options(verb_token, "always")

    pprint(verb_forms)
    pprint(related_words)
    pprint(verb_options)
