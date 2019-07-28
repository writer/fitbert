import re

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
            verb_forms.append(
                ["", "", VBP, "present simple", "present", "active", ["1S"]]
            )  # write
            verb_forms.append(
                [
                    "",
                    "",
                    "are",
                    "present simple",
                    "present",
                    "active",
                    ["2S", "1P", "2P", "3P"],
                ]
            )  # write
        else:
            verb_forms.append(
                [
                    "",
                    "",
                    VBP,
                    "present simple",
                    "present",
                    "active",
                    ["1S", "2S", "1P", "2P", "3P"],
                ]
            )  # write
        verb_forms.append(
            ["", "", VBZ, "present simple", "present", "active", ["3S"]]
        )  # writes
        verb_forms.append(
            ["am", "", VBN, "present simple", "present", "passive", ["1S"]]
        )  # am written
        verb_forms.append(
            ["is", "", VBN, "present simple", "present", "passive", ["3S"]]
        )  # is written
        verb_forms.append(
            [
                "are",
                "",
                VBN,
                "present simple",
                "present",
                "passive",
                ["2S", "1P", "2P", "3P"],
            ]
        )  # are written
        verb_forms.append(
            ["am", "", VBG, "present continuous", "present", "active", ["1S"]]
        )  # am writing
        verb_forms.append(
            ["is", "", VBG, "present continuous", "present", "active", ["3S"]]
        )  # is writing
        verb_forms.append(
            [
                "are",
                "",
                VBG,
                "present continuous",
                "present",
                "active",
                ["2S", "1P", "2P", "3P"],
            ]
        )  # are writing
        verb_forms.append(
            ["am", "being", VBN, "present continuous", "present", "passive", ["1S"]]
        )  # am being written
        verb_forms.append(
            ["is", "being", VBN, "present continuous", "present", "passive", ["3S"]]
        )  # is being written
        verb_forms.append(
            [
                "are",
                "being",
                VBN,
                "present continuous",
                "present",
                "passive",
                ["2S", "1P", "2P", "3P"],
            ]
        )  # are being written
        verb_forms.append(
            [
                "",
                "",
                VBD,
                "past simple",
                "past",
                "active",
                ["1S", "2S", "3S", "1P", "2P", "3P"],
            ]
        )  # wrote
        verb_forms.append(
            ["was", "", VBN, "past simple", "past", "passive", ["1S", "3S"]]
        )  # was written
        verb_forms.append(
            [
                "were",
                "",
                VBN,
                "past simple",
                "past",
                "passive",
                ["2S", "1P", "2P", "3P"],
            ]
        )  # were written
        verb_forms.append(
            ["was", "", VBG, "past continuous", "past", "active", ["1S", "3S"]]
        )  # was writing
        verb_forms.append(
            [
                "were",
                "",
                VBG,
                "past continuous",
                "past",
                "active",
                ["2S", "1P", "2P", "3P"],
            ]
        )  # were writing
        verb_forms.append(
            ["was", "being", VBN, "past continuous", "past", "passive", ["1S", "3S"]]
        )  # was being written
        verb_forms.append(
            [
                "were",
                "being",
                VBN,
                "past continuous",
                "past",
                "passive",
                ["2S", "1P", "2P", "3P"],
            ]
        )  # were being written
        verb_forms.append(
            [
                "have",
                "",
                VBN,
                "present perfect simple",
                "present",
                "active",
                ["1S", "2S", "1P", "2P", "3P"],
            ]
        )  # have written
        verb_forms.append(
            ["has", "", VBN, "present perfect simple", "present", "active", ["3S"]]
        )  # has written
        verb_forms.append(
            [
                "have",
                "been",
                VBN,
                "present perfect simple",
                "present",
                "passive",
                ["1S", "2S", "1P", "2P", "3P"],
            ]
        )  # have been written
        verb_forms.append(
            ["has", "been", VBN, "present perfect simple", "present", "passive", ["3S"]]
        )  # has been written
        verb_forms.append(
            [
                "have",
                "been",
                VBG,
                "present perfect continuous",
                "present",
                "active",
                ["1S", "2S", "1P", "2P", "3P"],
            ]
        )  # have been writing
        verb_forms.append(
            [
                "has",
                "been",
                VBG,
                "present perfect continuous",
                "present",
                "active",
                ["3S"],
            ]
        )  # has been writing
        verb_forms.append(
            [
                "have",
                "been being",
                VBN,
                "present perfect continuous",
                "present",
                "passive",
                ["1S", "2S", "1P", "2P", "3P"],
            ]
        )  # have been being written
        verb_forms.append(
            [
                "has",
                "been being",
                VBN,
                "present perfect continuous",
                "present",
                "passive",
                ["3S"],
            ]
        )  # has been being written
        verb_forms.append(
            [
                "had",
                "",
                VBN,
                "past perfect simple",
                "past",
                "active",
                ["1S", "2S", "3S", "1P", "2P", "3P"],
            ]
        )  # had written
        verb_forms.append(
            [
                "had",
                "been",
                VBN,
                "past perfect simple",
                "past",
                "passive",
                ["1S", "2S", "3S", "1P", "2P", "3P"],
            ]
        )  # had been written
        verb_forms.append(
            [
                "had",
                "been",
                VBG,
                "past perfect continuous",
                "past",
                "active",
                ["1S", "2S", "3S", "1P", "2P", "3P"],
            ]
        )  # had been writing
        verb_forms.append(
            [
                "had",
                "been",
                VBN,
                "past perfect continuous",
                "past",
                "passive",
                ["1S", "2S", "3S", "1P", "2P", "3P"],
            ]
        )  # had been written
        verb_forms.append(
            [
                "will",
                "",
                VB,
                "future simple",
                "future",
                "active",
                ["1S", "2S", "3S", "1P", "2P", "3P"],
            ]
        )  # will write
        verb_forms.append(
            [
                "will",
                "be",
                VBN,
                "future simple",
                "future",
                "passive",
                ["1S", "2S", "3S", "1P", "2P", "3P"],
            ]
        )  # will be written
        verb_forms.append(
            [
                "will",
                "be",
                VBG,
                "future continuous",
                "future",
                "active",
                ["1S", "2S", "3S", "1P", "2P", "3P"],
            ]
        )  # will be writing
        verb_forms.append(
            [
                "will",
                "be being",
                VBN,
                "future continuous",
                "future",
                "passive",
                ["1S", "2S", "3S", "1P", "2P", "3P"],
            ]
        )  # will be being written
        verb_forms.append(
            [
                "will",
                "have",
                VBN,
                "future perfect simple",
                "future",
                "active",
                ["1S", "2S", "3S", "1P", "2P", "3P"],
            ]
        )  # will have written
        verb_forms.append(
            [
                "will",
                "have been",
                VBN,
                "future perfect simple",
                "future",
                "passive",
                ["1S", "2S", "3S", "1P", "2P", "3P"],
            ]
        )  # will have been written
        verb_forms.append(
            [
                "will",
                "have been",
                VBG,
                "future perfect continuous",
                "future",
                "active",
                ["1S", "2S", "3S", "1P", "2P", "3P"],
            ]
        )  # will have been writing
        verb_forms.append(
            [
                "will",
                "have been being",
                VBN,
                "future perfect continuous",
                "future",
                "passive",
                ["1S", "2S", "3S", "1P", "2P", "3P"],
            ]
        )  # will have been being written

    return verb_forms


def get_verb_options(
    verb, verb_phrase_inffix="", tense=["present", "past", "future"], form=["active"]
):
    verb_forms = conjugate(verb)
    options = []
    diff_order = ["there", "here", "everywhere", "elsewhere", "anywhere", "nowhere"]
    for verb_form in verb_forms:
        if (verb_form[4] in tense) and (verb_form[5] in form):
            if verb_phrase_inffix.lower() in diff_order:
                elements = [verb_phrase_inffix, verb_form[0]] + verb_form[1:3]
            else:
                elements = [verb_form[0], verb_phrase_inffix] + verb_form[1:3]
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

    print(verb_forms)
    print(related_words)
