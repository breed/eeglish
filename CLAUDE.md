# project description

create a website and a tool that will convert standard american spelling to ingglish spelling.

## ingglish spelling rules

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
- don't translate HTML tags or special markdown keys or tags
- see `ALFUBET.md` for the full letter mapping and `RULES.md` for detailed rules with examples

## files

- `ALFUBET.md` - IPA-to-ingglish letter mapping (24 consonants, 17 vowels)
- `RULES.md` - detailed explanation of the spelling rules with examples
- `DIKSHUNEREE.md` - 126,052 word dictionary with columns `english`, `ingglish`, `IPA`
- `dikshuneree.json` - JSON version of the dictionary for the website
- `tranzlaet.py` - CLI tool that translates english text to ingglish (`python3 tranzlaet.py [file...]` or stdin)
- `index.html` - website for translating pasted text or fetched URLs to ingglish (serve with `python3 -m http.server`)

## regenerating the dictionary

the dictionary was generated from the CMU Pronouncing Dictionary. to regenerate `DIKSHUNEREE.md`, create a python venv, install `cmudict`, and run a script that:
1. maps ARPABET phonemes → ingglish letters using `ALFUBET.md`
2. maps ARPABET phonemes → IPA symbols for the IPA column
3. handles Y + UW → "ue" (the /juː/ sound)
4. strips stress markers (0, 1, 2) from ARPABET codes
5. takes first pronunciation when multiple exist
6. both DH and TH map to `th`

after regenerating `DIKSHUNEREE.md`, regenerate `dikshuneree.json` for the website

## changing letter mappings

when a letter-to-sound mapping changes:
1. update `ALFUBET.md`
2. update `RULES.md`
3. regenerate ingglish column in `DIKSHUNEREE.md` from the IPA column using updated mappings
4. regenerate `dikshuneree.json` from `DIKSHUNEREE.md`
5. update this file

the IPA-to-ingglish converter for regenerating the dictionary:

```python
IPA_TO_ING = [
    ('juː', 'ue'), ('tʃ', 'ch'), ('dʒ', 'j'), ('eɪ', 'ae'), ('iː', 'ee'),
    ('aɪ', 'ie'), ('oʊ', 'oe'), ('ɔː', 'o'), ('uː', 'oo'), ('aʊ', 'ou'),
    ('ɔɪ', 'oi'), ('ɝ', 'yr'),
    ('ð', 'th'), ('ŋ', 'ng'), ('ʃ', 'sh'), ('θ', 'th'), ('ʒ', 'zj'),
    ('ɡ', 'g'), ('ɹ', 'r'), ('æ', 'a'), ('ɛ', 'e'), ('ɪ', 'i'),
    ('ɑ', 'aa'), ('ʌ', 'u'), ('ə', 'u'), ('ʊ', 'uu'),
    ('b', 'b'), ('d', 'd'), ('f', 'f'), ('h', 'h'), ('j', 'y'),
    ('k', 'k'), ('l', 'l'), ('m', 'm'), ('n', 'n'), ('p', 'p'),
    ('s', 's'), ('t', 't'), ('v', 'v'), ('w', 'w'), ('z', 'z'),
]
```

order matters — longest IPA sequences must come first for greedy matching.

## translation tools

- `tranzlaet.py` and `index.html` both do word-by-word dictionary lookup
- HTML tags and markdown syntax pass through untranslated
- capitalization is preserved (ALL CAPS, Title Case, lowercase)
- the tokenizer splits on `<` so text adjacent to HTML tags is handled correctly
