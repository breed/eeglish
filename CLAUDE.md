# project description

a website and tools that convert standard american spelling to inglish spelling.

the site is live at https://inglish.us (github pages from this repo).

## inglish spelling rules

see `RULES.md` for the full spelling rules and `ALFUBET.md` for the IPA-to-inglish letter mapping.

key points for tools and dictionary generation:
- don't translate acronyms — they are excluded from the dictionary
- don't translate HTML tags or special markdown keys or tags

## files

- `ALFUBET.md` - IPA-to-inglish letter mapping (24 consonants, 17 vowels)
- `RULES.md` - detailed explanation of the spelling rules with examples
- `DIKSHUNEREE.md` - 125,873 word dictionary with columns `english`, `inglish`, `IPA`
- `dikshuneree.json` - JSON version of the dictionary for the website
- `generate_dictionary.py` - regenerates `DIKSHUNEREE.md` and `dikshuneree.json` from CMU Pronouncing Dictionary
- `tranzlaet.py` - CLI tool that translates english text to inglish (`python3 tranzlaet.py [file...]` or stdin)
- `index.html` - website with translate tab (paste text) and rules reference tab
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

## changing letter mappings

when a letter-to-sound mapping changes:
1. update `ALFUBET.md`
2. update `RULES.md`
3. update the mapping in `generate_dictionary.py`
4. run `generate_dictionary.py` to regenerate `DIKSHUNEREE.md` and `dikshuneree.json`
5. update the rules tab content in `index.html`
6. update this file

## translation tools

- `tranzlaet.py` and `index.html` both do word-by-word dictionary lookup
- HTML tags and markdown syntax pass through untranslated
- capitalization is preserved (ALL CAPS, Title Case, lowercase)
- the tokenizer splits on `<` so text adjacent to HTML tags is handled correctly
