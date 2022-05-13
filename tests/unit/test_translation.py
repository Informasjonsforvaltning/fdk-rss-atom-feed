from fdk_rss_atom_feed.translation import translate, translate_or_emptystr
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
    try:
        translate({"es": "", "nb": ""})
        raise AssertionError("translate should raise exception")
    except ValueError as e:
        assert "Translatable does not contain any translations" in str(e)
    try:
        translate({})
        raise AssertionError("translate should raise exception")
    except ValueError as e:
        assert "Translatable does not contain any translations" in str(e)


@pytest.mark.unit
def test_translate_or_emptystr_with_no_translation() -> None:
    assert translate_or_emptystr({"es": "", "nb": ""}) == ""
    assert translate_or_emptystr({}) == ""
