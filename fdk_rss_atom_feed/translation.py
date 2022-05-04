import logging
from typing import Dict


def translate(translatable: Dict[str, str]) -> str:
    languages = ["nb", "no", "nn", "en"]

    # supported languages in preferred order
    for lang in languages:
        if lang in translatable and translatable[lang] != "":
            return translatable[lang]

    # any language that has a translation
    for translation in translatable.values():
        if translation != "":
            return translation

    logging.error("No translation found")
    return ""
