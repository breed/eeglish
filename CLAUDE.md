# project description

a website and tools that convert standard american spelling to inglish spelling.

the site is live at https://inglish.org (github pages from this repo).

## inglish spelling rules

- all letters and letter combinations have exactly one sound
- the assignment of a letter or letter combination to a sound should be close to what is currently in use
- vowel sounds only change based on immediately adjacent vowel
- the common short sound of a vowel happens when the vowel is by itself
- `o` by itself makes the /ɔː/ sound as in `dog`, `for`
- `aa` (doubled a) makes the /ɑ/ sound as in `hot` → `haat`
- if a vowel is immediately followed by an e the vowel will sound like its name
- `yr` is the r-colored vowel /ɝ/ as in `bird` → `byrd`
- `zj` is the /ʒ/ sound as in `measure` → `mezjyr`
- `th` is used for both voiced (ð) and voiceless (θ) th sounds
- first diphthong wins — read left to right, greedily match the first vowel pair
- when multiple pronunciations exist, pick the one whose inglish spelling is closest to the english spelling (edit distance)
- don't translate HTML tags or special markdown keys or tags
- see `ALFUBET.md` for the full letter mapping and `RULES.md` for detailed rules with examples

## files

- `ALFUBET.md` - IPA-to-inglish letter mapping (24 consonants, 17 vowels)
- `RULES.md` - detailed explanation of the spelling rules with examples
- `DIKSHUNEREE.md` - 126,052 word dictionary with columns `english`, `inglish`, `IPA`
- `dikshuneree.json` - JSON version of the dictionary for the website
- `generate_dictionary.py` - regenerates `DIKSHUNEREE.md` and `dikshuneree.json` from CMU Pronouncing Dictionary
- `tranzlaet.py` - CLI tool that translates english text to inglish (`python3 tranzlaet.py [file...]` or stdin)
- `index.html` - website with translate tab (paste text) and rules reference tab
- `CNAME` - custom domain config for github pages (inglish.org)

## regenerating the dictionary

run `generate_dictionary.py` in a venv with `cmudict` installed:

```
python3 -m venv venv
venv/bin/pip install cmudict
venv/bin/python3 generate_dictionary.py
```

this regenerates both `DIKSHUNEREE.md` and `dikshuneree.json`.

the script:
1. maps ARPABET phonemes → inglish letters
2. maps ARPABET phonemes → IPA symbols for the IPA column
3. handles Y + UW → "ue" (the /juː/ sound)
4. strips stress markers (0, 1, 2) from ARPABET codes
5. when multiple pronunciations exist, picks the one whose inglish spelling is closest to the english spelling (levenshtein distance)
6. both DH and TH map to `th`

## changing letter mappings

when a letter-to-sound mapping changes:
1. update `ALFUBET.md`
2. update `RULES.md`
3. update the mapping in `generate_dictionary.py`
4. run `generate_dictionary.py` to regenerate `DIKSHUNEREE.md` and `dikshuneree.json`
5. update this file

## translation tools

- `tranzlaet.py` and `index.html` both do word-by-word dictionary lookup
- HTML tags and markdown syntax pass through untranslated
- capitalization is preserved (ALL CAPS, Title Case, lowercase)
- the tokenizer splits on `<` so text adjacent to HTML tags is handled correctly
