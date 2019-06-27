from fitbert.delemmatize import Delemmatizer


dl = Delemmatizer()


def test_delemmatizer_instantiates():
    assert Delemmatizer() is not None, "It instantiates"


def test_delemmatizer_callable():
    assert callable(dl), "Delemmatizer instance should be callable"


def test_delemmatizes_lemmas():
    assert dl("look") == ["looked", "looking", "looks"], "should delemmatize lemmas"


def test_delemmatizes_non_lemmas():
    assert dl("running") == ["ran", "running", "runs"], "should delemmatize non-lemmas"
