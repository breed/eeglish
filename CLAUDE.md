# project description

a website and tools that convert standard american spelling to inglish spelling.

the site is live at https://inglish.us (github pages from this repo).

## inglish spelling rules

`RULES.md` is the single source of truth for all spelling rules. `ALFUBET.md` has the IPA-to-inglish letter mapping table.

key points for tools and dictionary generation:
- don't translate acronyms — they are excluded from the dictionary
- don't translate HTML tags or special markdown keys or tags

## files

- `ALFUBET.md` - IPA-to-inglish letter mapping (24 consonants, 17 vowels)
- `RULES.md` - single source of truth for spelling rules, with examples
- `DIKSHUNEREE.md` - 125,858 word dictionary with columns `english`, `inglish`, `IPA`
- `dikshuneree.json` - JSON version of the dictionary for the website
- `generate_dictionary.py` - regenerates `DIKSHUNEREE.md` and `dikshuneree.json` from CMU Pronouncing Dictionary
- `tranzlaet.py` - CLI tool that translates english text to inglish (`python3 tranzlaet.py [file...]` or stdin)
- `index.html` - website with translate tab (paste text) and rules tab (auto-rendered from RULES.md)
- `translate-button.js` - embeddable script that adds a floating inglish translate button to any webpage
- `CNAME` - custom domain config for github pages (inglish.us)

## regenerating the dictionary

run `generate_dictionary.py` in a venv with `cmudict` installed:

```
python3 -m venv venv
venv/bin/pip install cmudict
venv/bin/python3 generate_dictionary.py
```

this regenerates both `DIKSHUNEREE.md` and `dikshuneree.json`.

the script applies all rules from `RULES.md`, including:
1. maps ARPABET phonemes → inglish letters and IPA symbols
2. handles Y + UW → "ue" (the /juː/ sound)
3. words spelled with `aw` get `aa` instead of `o` for the AO phoneme
4. picks closest pronunciation by edit distance; breaks ties by preferring ɑ (AA) over ɔː (AO)
5. excludes acronyms (words whose only pronunciations are letter-by-letter spellings)
6. preserves contractions: translates the base word, keeps the apostrophe and suffix ('t, 's, 'd, 'm, 'l, 'r, 'v)
7. skips leading-apostrophe words ('em, 'twas, etc.) — they pass through the translator unchanged

## changing letter mappings

when a letter-to-sound mapping changes:
1. update `ALFUBET.md`
2. update `RULES.md`
3. update the mapping in `generate_dictionary.py`
4. run `generate_dictionary.py` to regenerate `DIKSHUNEREE.md` and `dikshuneree.json`
5. update this file
6. no need to update `index.html` — the rules tab auto-renders `RULES.md`

## changing spelling rules

when a spelling rule changes (contractions, alternate pronunciation selection, aw→aa, etc.):
1. update `RULES.md` (source of truth)
2. update the logic in `generate_dictionary.py`
3. run `generate_dictionary.py` to regenerate the dictionary
4. verify examples in `RULES.md` and `ALFUBET.md` match the regenerated dictionary
5. update this file if the script behavior summary above needs changes
6. no need to update `index.html` — the rules tab auto-renders `RULES.md`

## translation tools

- `tranzlaet.py` and `index.html` both do word-by-word dictionary lookup from `dikshuneree.json`
- HTML tags and markdown syntax pass through untranslated
- capitalization is preserved (ALL CAPS, Title Case, lowercase)
- contractions (don't, I'm, we're, etc.) are looked up as whole tokens — the dictionary already has them with apostrophes preserved
- the tokenizer regex is `<[^>]*>|[^<\s]+|\s+` — splits on whitespace and HTML tags
- the punctuation regex `^([^\w]*)(\w.*\w|\w)([^\w]*)$` strips leading/trailing non-word characters before dictionary lookup

## website rules tab

the rules tab in `index.html` fetches `RULES.md` at runtime and renders it to HTML using a simple inline markdown parser. this means the rules tab is always in sync with `RULES.md` — no manual HTML updates needed.

the markdown parser handles: headings, tables, bold, code, links, ordered/numbered lists (with nested sub-bullets), and paragraphs. if new markdown features are added to `RULES.md` (e.g. blockquotes, images), the parser in `index.html` may need to be extended.
