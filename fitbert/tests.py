import json

import pytest
from fitbert import FitBert
from fitbert.delemmatize import Delemmatizer

dl = Delemmatizer()


def test_delemmatizer_instantiates():
    assert Delemmatizer() is not None, "It instantiates"


def test_delemmatizer_callable():
    assert callable(dl), "Delemmatizer instance should be callable"


def test_delemmatizes_lemmas():
    assert dl("look") == [
        "looked",
        "looking",
        "looks",
        "look",
    ], "should delemmatize lemmas"


def test_delemmatizes_non_lemmas():
    assert dl("ran") == [
        "ran",
        "running",
        "runs",
        "run",
    ], "should delemmatize non-lemmas"


"""
def test_masker_works_without_instantiating():
    masked_string, masked = FitBert.mask(
        "This might be justified to signalling the connection between drunken driving and fatal accidents.",
        (27, 37),
    )
    assert FitBert.mask_token in masked_string, "It should mask using the mask token"
    assert masked == "signalling", "It should mask the write substring"
"""


@pytest.mark.slow
def test_ranking():
    fb = FitBert()
    assert callable(fb.fitb)

    sentences = [
                    "When she started talking about her ex-boyfriends, he looked like a ***mask*** out of water",
                    "The boy was warned that if he misbehaved in the class, he would have to pay ***mask***.",
                    "I am surprised that you have ***mask*** patience.",
                ]

    options =   [
                    ["frog", "fish"],
                    ["the drummer", "the flutist", "the piper"],
                    ["such a", "so", "such"],
                ]
    answers =   [
                    "fish",
                    "the piper",
                    "such",
                ]
    for sentence, option, answer in zip(sentences, options, answers):
        ranked_options = fb.rank_multi(sentence, option)
        assert ranked_options[0] == answer, "It should rank options"
