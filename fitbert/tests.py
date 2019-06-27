import pytest

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


from fitbert import FitBert


def test_masker_works_without_instantiating():
    masked_string, masked = FitBert.mask(
        "This might be justified to signalling the connection between drunken driving and fatal accidents.",
        (27, 37),
    )
    assert FitBert.mask_token in masked_string, "It should mask using the mask token"
    assert masked == "signalling", "It should mask the write substring"


@pytest.mark.slow
def test_fitb_initializes():
    fb = FitBert()
    assert callable(fb.fitb)
