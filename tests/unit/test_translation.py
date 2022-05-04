from fdk_rss_atom_feed.translation import translate
import pytest


@pytest.mark.unit
def test_translation_with_preferred_languages() -> None:
    assert translate({"nb": "hei", "en": "hi"}) == "hei"
    assert translate({"en": "hi", "nb": "hei"}) == "hei"
    assert translate({"en": "hi", "nb": ""}) == "hi"
    assert translate({"es": "hola", "en": "hi"}) == "hi"


@pytest.mark.unit
def test_translation_with_other_languages() -> None:
    assert translate({"es": "hola", "fr": "bonjour"}) == "hola"
    assert translate({"fr": "bonjour", "es": "hola"}) == "bonjour"


@pytest.mark.unit
def test_translation_with_no_translation() -> None:
    assert translate({"es": "", "nb": ""}) == ""
    assert translate({}) == ""
