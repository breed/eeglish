#!/usr/bin/env python3
"""tranzlaet - translate english text to inglish spelling."""

import argparse
import json
import os
import re
import sys


def data_path(name):
    """Locate a data file next to this module (git checkout) or in the
    inglish_data directory (installed PyPI wheel)."""
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, name)
    if os.path.exists(path):
        return path
    return os.path.join(here, "inglish_data", name)


def load_dictionary():
    """Load dikshuneree.json into a dict mapping english -> inglish."""
    with open(data_path("dikshuneree.json"), encoding="utf-8") as f:
        return json.load(f)


def apply_capitalization(original, translated):
    """Preserve the capitalization pattern of the original word.

    A single capital letter is title case, not ALL CAPS ("I" → "Ie").
    """
    if original.isupper() and len(original) > 1:
        return translated.upper()
    if original[0].isupper() and (len(original) == 1 or original[1:].islower()):
        return translated.capitalize()
    return translated


# regex: HTML tags, runs of non-whitespace (stopping at <), a lone <, or whitespace
_TOKEN_RE = re.compile(r"<[^>]*>|[^<\s]+|<|\s+")
# leading/trailing punctuation
_PUNCT_RE = re.compile(r"^([^\w]*)(\w.*\w|\w)([^\w]*)$", re.UNICODE)


def translate_text(text, dictionary):
    """Translate a string from english to inglish, preserving structure."""
    tokens = _TOKEN_RE.findall(text)
    result = []
    for token in tokens:
        # pass through whitespace and HTML tags
        if token.isspace() or (token.startswith("<") and token.endswith(">")):
            result.append(token)
            continue
        # try to split off surrounding punctuation
        m = _PUNCT_RE.match(token)
        if not m:
            # all punctuation / no word chars — pass through
            result.append(token)
            continue
        leading, word, trailing = m.groups()
        # curly apostrophes match the ASCII-apostrophe dictionary entries
        lookup = word.lower().replace("’", "'")
        # dictionary keys can end in an apostrophe (plural possessives, goin')
        if trailing[:1] in ("'", "’") and lookup + "'" in dictionary:
            word += trailing[0]
            trailing = trailing[1:]
            lookup += "'"
        if lookup in dictionary:
            translated = apply_capitalization(word, dictionary[lookup])
            if "’" in word:
                translated = translated.replace("'", "’")
            result.append(leading + translated + trailing)
        else:
            result.append(token)
    return "".join(result)


def main():
    parser = argparse.ArgumentParser(
        description="Translate english text to inglish spelling."
    )
    parser.add_argument(
        "files",
        nargs="*",
        type=argparse.FileType("r", encoding="utf-8"),
        default=[sys.stdin],
        help="Files to translate (default: stdin)",
    )
    args = parser.parse_args()

    dictionary = load_dictionary()

    for f in args.files:
        for line in f:
            sys.stdout.write(translate_text(line, dictionary))


if __name__ == "__main__":
    main()
