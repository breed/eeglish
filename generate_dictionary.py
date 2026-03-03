#!/usr/bin/env python3
"""Generate DIKSHUNEREE.md from the CMU Pronouncing Dictionary.

When multiple pronunciations exist for a word, picks the one whose
inglish spelling is closest to the original english spelling.
"""
import json
import re

try:
    import cmudict
except ImportError:
    print("Install cmudict first: pip install cmudict")
    raise SystemExit(1)

# ARPABET (without stress) → inglish
ARPABET_TO_ING = {
    'AA': 'aa', 'AE': 'a', 'AH': 'u', 'AO': 'o', 'AW': 'ou',
    'AY': 'ie', 'B': 'b', 'CH': 'ch', 'D': 'd', 'DH': 'th',
    'EH': 'e', 'ER': 'yr', 'EY': 'ae', 'F': 'f', 'G': 'g',
    'HH': 'h', 'IH': 'i', 'IY': 'ee', 'JH': 'j', 'K': 'k',
    'L': 'l', 'M': 'm', 'N': 'n', 'NG': 'ng', 'OW': 'oe',
    'OY': 'oi', 'P': 'p', 'R': 'r', 'S': 's', 'SH': 'sh',
    'T': 't', 'TH': 'th', 'UH': 'uu', 'UW': 'oo', 'V': 'v',
    'W': 'w', 'Y': 'y', 'Z': 'z', 'ZH': 'zj',
}

# ARPABET (without stress) → IPA
ARPABET_TO_IPA = {
    'AA': 'ɑ', 'AE': 'æ', 'AH': 'ʌ', 'AO': 'ɔː', 'AW': 'aʊ',
    'AY': 'aɪ', 'B': 'b', 'CH': 'tʃ', 'D': 'd', 'DH': 'ð',
    'EH': 'ɛ', 'ER': 'ɝ', 'EY': 'eɪ', 'F': 'f', 'G': 'ɡ',
    'HH': 'h', 'IH': 'ɪ', 'IY': 'iː', 'JH': 'dʒ', 'K': 'k',
    'L': 'l', 'M': 'm', 'N': 'n', 'NG': 'ŋ', 'OW': 'oʊ',
    'OY': 'ɔɪ', 'P': 'p', 'R': 'ɹ', 'S': 's', 'SH': 'ʃ',
    'T': 't', 'TH': 'θ', 'UH': 'ʊ', 'UW': 'uː', 'V': 'v',
    'W': 'w', 'Y': 'j', 'Z': 'z', 'ZH': 'ʒ',
}


def strip_stress(phoneme):
    """Remove stress marker (0, 1, 2) from ARPABET phoneme."""
    return re.sub(r'[012]$', '', phoneme)


def phonemes_to_inglish(phonemes):
    """Convert ARPABET phoneme list to inglish spelling."""
    stripped = [strip_stress(p) for p in phonemes]
    result = []
    i = 0
    while i < len(stripped):
        # handle Y + UW → "ue" (the /juː/ sound)
        if stripped[i] == 'Y' and i + 1 < len(stripped) and stripped[i + 1] == 'UW':
            result.append('ue')
            i += 2
        else:
            result.append(ARPABET_TO_ING.get(stripped[i], ''))
            i += 1
    return ''.join(result)


def phonemes_to_ipa(phonemes):
    """Convert ARPABET phoneme list to IPA string."""
    stripped = [strip_stress(p) for p in phonemes]
    result = []
    i = 0
    while i < len(stripped):
        if stripped[i] == 'Y' and i + 1 < len(stripped) and stripped[i + 1] == 'UW':
            result.append('juː')
            i += 2
        else:
            result.append(ARPABET_TO_IPA.get(stripped[i], ''))
            i += 1
    return ''.join(result)


def edit_distance(a, b):
    """Levenshtein distance between two strings."""
    m, n = len(a), len(b)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, n + 1):
            temp = dp[j]
            if a[i - 1] == b[j - 1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(prev, dp[j], dp[j - 1])
            prev = temp
    return dp[n]


def main():
    d = cmudict.dict()

    entries = []
    multi_count = 0
    changed_count = 0

    for word in sorted(d.keys()):
        pronunciations = d[word]

        if len(pronunciations) == 1:
            ing = phonemes_to_inglish(pronunciations[0])
            ipa = phonemes_to_ipa(pronunciations[0])
            entries.append((word, ing, ipa))
        else:
            multi_count += 1
            # pick the pronunciation whose inglish is closest to the english
            best_ing = None
            best_ipa = None
            best_dist = float('inf')
            first_ing = None

            for pron in pronunciations:
                ing = phonemes_to_inglish(pron)
                ipa = phonemes_to_ipa(pron)
                dist = edit_distance(word, ing)

                if first_ing is None:
                    first_ing = ing

                if dist < best_dist:
                    best_dist = dist
                    best_ing = ing
                    best_ipa = ipa

            if best_ing != first_ing:
                changed_count += 1

            entries.append((word, best_ing, best_ipa))

    # write DIKSHUNEREE.md
    with open('DIKSHUNEREE.md', 'w', encoding='utf-8') as f:
        f.write('# dictionary\n\n')
        f.write('inglish dictionary generated from the CMU Pronouncing Dictionary.\n\n')
        f.write('| english | inglish | IPA |\n')
        f.write('|---------|---------|-----|\n')
        for word, ing, ipa in entries:
            f.write(f'| {word} | {ing} | {ipa} |\n')

    # write dikshuneree.json
    dictionary = {word: ing for word, ing, ipa in entries}
    with open('dikshuneree.json', 'w', encoding='utf-8') as f:
        json.dump(dictionary, f, ensure_ascii=False, separators=(',', ':'))

    print(f'total entries: {len(entries)}')
    print(f'words with multiple pronunciations: {multi_count}')
    print(f'words where alternate pronunciation was chosen: {changed_count}')

    # spot check
    for w in ['hello', 'the', 'hot', 'dog', 'bird', 'world', 'measure',
              'cat', 'go', 'food', 'law', 'thought']:
        if w in dictionary:
            print(f'  {w} → {dictionary[w]}')


if __name__ == '__main__':
    main()
