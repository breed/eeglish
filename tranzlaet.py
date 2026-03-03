#!/usr/bin/env python3
"""tranzlaet - translate english text to inglish spelling."""

import argparse
import os
import re
import sys


def load_dictionary(path):
    """Parse DIKSHUNEREE.md into a dict mapping english -> inglish."""
    dictionary = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("|"):
                continue
            parts = [p.strip() for p in line.split("|")]
            # parts[0] is empty (before first |), parts[1] = english, parts[2] = inglish
            if len(parts) < 4:
                continue
            english = parts[1]
            inglish = parts[2]
            # skip header rows
            if english.startswith("---") or parts[3] == "IPA":
                continue
            dictionary[english.lower()] = inglish
    return dictionary


def apply_capitalization(original, translated):
    """Preserve the capitalization pattern of the original word."""
    if original.isupper():
        return translated.upper()
    if original[0].isupper() and original[1:].islower():
        return translated.capitalize()
    return translated


# regex: HTML tags, or runs of non-whitespace (stopping at <), or runs of whitespace
_TOKEN_RE = re.compile(r"<[^>]*>|[^<\s]+|\s+")
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
        lookup = word.lower()
        if lookup in dictionary:
            translated = apply_capitalization(word, dictionary[lookup])
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

    dict_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DIKSHUNEREE.md")
    dictionary = load_dictionary(dict_path)

    for f in args.files:
        for line in f:
            sys.stdout.write(translate_text(line, dictionary))


if __name__ == "__main__":
    main()
