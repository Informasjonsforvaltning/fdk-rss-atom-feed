import logging
import traceback
from typing import Dict, Optional


def translate_or_emptystr(translatable: Optional[Dict[str, str]]) -> str:
    try:
        return translate(translatable)
    except ValueError:
        logging.error(f"{traceback.format_exc()}Error translating: {str(translatable)}")
    return ""


def translate(translatable: Optional[Dict[str, str]]) -> str:
    languages = ["nb", "no", "nn", "en"]

    if translatable:
        # supported languages in preferred order
        for lang in languages:
            if lang in translatable and translatable[lang] != "":
                return translatable[lang]

        # any language that has a translation
        for translation in translatable.values():
            if translation != "":
                return translation

    raise ValueError("Translatable does not contain any translations")
