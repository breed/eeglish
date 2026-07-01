#!/usr/bin/env python3
"""Tests for tranzlaet.py."""

import json
import os
import unittest

from tranzlaet import apply_capitalization, translate_text


class TestApplyCapitalization(unittest.TestCase):
    def test_single_capital_letter_is_title_case(self):
        # "I" is title case, not ALL CAPS — it should become "Ie", not "IE"
        self.assertEqual(apply_capitalization("I", "ie"), "Ie")

    def test_all_caps(self):
        self.assertEqual(apply_capitalization("HELLO", "heloe"), "HELOE")

    def test_all_caps_contraction(self):
        self.assertEqual(apply_capitalization("DON'T", "doen't"), "DOEN'T")

    def test_title_case(self):
        self.assertEqual(apply_capitalization("Hello", "heloe"), "Heloe")

    def test_lowercase(self):
        self.assertEqual(apply_capitalization("hello", "heloe"), "heloe")


class TestTranslateText(unittest.TestCase):
    DICT = {
        "hello": "heloe",
        "don't": "doen't",
        "ol'": "oel'",
        "goin'": "goeun'",
        "goin": "goin",
        "lawyers": "laayyrz",
        "lawyers'": "laayyrz'",
    }

    def test_lone_less_than_is_preserved(self):
        # a "<" with no closing ">" must not be dropped from the output
        self.assertEqual(translate_text("5 < 10", self.DICT), "5 < 10")
        self.assertEqual(translate_text("3<4", self.DICT), "3<4")

    def test_html_tag_passes_through(self):
        self.assertEqual(translate_text("<b>hello</b>", self.DICT), "<b>heloe</b>")

    def test_curly_apostrophe_contraction(self):
        # don’t (U+2019) should match the ASCII-apostrophe dictionary entry
        # and keep the curly apostrophe in the output
        self.assertEqual(translate_text("don’t", self.DICT), "doen’t")

    def test_trailing_apostrophe_word(self):
        # dictionary keys ending in an apostrophe (goin', ol') must be reachable
        self.assertEqual(translate_text("ol' goin'", self.DICT), "oel' goeun'")

    def test_plural_possessive(self):
        self.assertEqual(translate_text("lawyers' fees", self.DICT), "laayyrz' fees")

    def test_single_quoted_word(self):
        # quoting apostrophes around a word are not part of it
        self.assertEqual(translate_text("'hello'", self.DICT), "'heloe'")


class TestRealDictionary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = os.path.join(os.path.dirname(__file__), "dikshuneree.json")
        with open(path) as f:
            cls.DICT = json.load(f)

    def test_ai_is_excluded(self):
        # "ai" (the sloth) is manually excluded so the acronym AI
        # passes through untranslated
        self.assertNotIn("ai", self.DICT)
        self.assertEqual(translate_text("AI is here", self.DICT), "AI iz heer")


if __name__ == "__main__":
    unittest.main()
