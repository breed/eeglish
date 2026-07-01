#!/usr/bin/env python3
"""Tests for inglish_mcp.py."""

import unittest

from inglish_mcp import (
    DICTIONARY,
    REVERSE,
    lookup_word,
    reverse_translate,
    translate,
)


class TestTranslate(unittest.TestCase):
    def test_acronym_passes_through(self):
        # "AI" is excluded from the dictionary; "is"/"here" translate
        self.assertEqual(translate("AI is here"), "AI iz heer")

    def test_title_case_preserved(self):
        self.assertEqual(translate("Hello"), "Heloe")


class TestLookupWord(unittest.TestCase):
    def test_known_word(self):
        self.assertEqual(
            lookup_word("hello"),
            {"english": "hello", "inglish": "heloe", "found": True},
        )

    def test_case_and_whitespace_normalized(self):
        self.assertEqual(lookup_word("  HELLO  ")["inglish"], "heloe")

    def test_unknown_word(self):
        result = lookup_word("zzzznotaword")
        self.assertFalse(result["found"])
        self.assertIsNone(result["inglish"])


class TestReverseTranslate(unittest.TestCase):
    def test_candidate_round_trips(self):
        # the inglish spelling of "here" must map back to "here"
        inglish = lookup_word("here")["inglish"]
        result = reverse_translate(inglish)
        self.assertIn("here", result["candidates"])

    def test_unknown_spelling(self):
        self.assertEqual(
            reverse_translate("zzzznotaspelling"),
            {"inglish": "zzzznotaspelling", "candidates": []},
        )


class TestIndexesLoaded(unittest.TestCase):
    def test_dictionary_loaded(self):
        self.assertGreater(len(DICTIONARY), 0)

    def test_reverse_index_loaded(self):
        self.assertGreater(len(REVERSE), 0)


if __name__ == "__main__":
    unittest.main()
