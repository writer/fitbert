import re

import numpy as np
import pyinflect
import spacy

from get_options import get_related_options, get_verb_options
from get_phrase import get_noun_phrase, get_verb_phrase


def mask_sentence(sentence_span, start, end, mask):
    masked_sentence_tok = [token.text for token in sentence_span]
    masked_sentence_tok[start] = mask
    masked_sentence_tok[start + 1 : end] = ""
    masked_sentence = re.sub(r"\s{2, }", " ", " ".join(masked_sentence_tok)).strip()
    return masked_sentence


def get_verb_gap(sentence_span, mask_token="***mask***"):

    verb_phrases = get_verb_phrase(sentence_span)

    if len(verb_phrases):
        chosen_verb_phrase = sorted(
            verb_phrases, key=lambda x: x["end"] - x["start"], reverse=True
        )[0]

        if len(chosen_verb_phrase["main_verb"]):
            main_verb = chosen_verb_phrase["main_verb"][0]
            answer = chosen_verb_phrase["verb_phrase"].text.lower()

            adverbs = chosen_verb_phrase["adverbs"]
            verb_phrase_inffix = " ".join([a.text for a in adverbs])

            start = chosen_verb_phrase["start"]
            end = chosen_verb_phrase["end"]

            options = get_verb_options(main_verb, verb_phrase_inffix)
            options_len = [1 / len(o) for o in options]
            options_prob = [o / sum(options_len) for o in options_len]

            if len(options) > 0:
                options = list(
                    np.random.choice(options, 3, p=options_prob, replace=False)
                )
                masked_sentence = mask_sentence(sentence_span, start, end, mask_token)

                if answer not in options:
                    options = options[:2]
                    options.append(answer)

                return masked_sentence, answer, options

    return None, None, None


def get_noun_gap(sentence_span, mask_token="***mask***"):

    noun_phrases = get_noun_phrase(sentence_span)

    if len(noun_phrases) > 0:
        chosen_noun_phrase = sorted(
            noun_phrases, key=lambda x: x["end"] - x["start"], reverse=True
        )[0]

        if len(chosen_noun_phrase["main_noun"]) > 0:
            main_noun = chosen_noun_phrase["main_noun"][0]
            answer = chosen_noun_phrase["noun_phrase"].text.lower()

            start = chosen_noun_phrase["start"]
            end = chosen_noun_phrase["end"]

            options = get_related_options(main_noun.text, True)
            np.random.shuffle(options)
            options = options[:3]

            masked_sentence = mask_sentence(sentence_span, start, end, mask_token)

            options_out = [answer.replace(main_noun.text, option) for option in options]

            if answer not in options_out:
                options_out = options_out[:2]
                options_out.append(answer)

            if len(options_out) > 1:
                return masked_sentence, answer, options_out

    return None, None, None


def get_prep_gap():
    return


if __name__ == "__main__":

    nlp = spacy.load("en_core_web_sm")

    sample_text = "Before we get into the gritty details of word embedding models, let us briefly talk about some language modelling fundamentals."

    doc = nlp(sample_text)

    for sentence in doc.sents:
        masked_sentence, answer, options = get_verb_gap(sentence)
        print(masked_sentence, answer, options)
