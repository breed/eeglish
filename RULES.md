# inglish spelling rules

inglish is a phonetic respelling of american english. every sound maps to exactly one spelling, and every spelling maps to exactly one sound. there are no silent letters, no irregular spellings, and no ambiguity.

## the core principle

**one sound = one spelling.** if you can read the letters, you can pronounce the word. if you can hear the word, you can spell it.

the letter assignments stay as close to standard english as possible so that inglish remains readable to english speakers.

## consonants

consonants work the way you'd expect from english. each consonant letter or pair makes one sound and only that sound.

| inglish | sound | english examples |
|----------|-------|-----------------|
| b | b as in bat | bat → bat |
| ch | ch as in chin | chin → chin |
| d | d as in dog | dog → dog |
| f | f as in fish | fish → fish |
| g | always hard g as in go | go → goe, get → get |
| h | h as in hat | hat → hat |
| j | j as in judge | judge → juj |
| k | k as in cat | cat → kat, cake → kaek |
| l | l as in lip | lip → lip |
| m | m as in map | map → map |
| n | n as in nap | nap → nap |
| ng | ng as in sing | sing → sing |
| p | p as in pen | pen → pen |
| r | r as in red | red → red |
| s | s as in sun | sun → sun |
| sh | sh as in ship | ship → ship |
| t | t as in top | top → top |
| th | th as in thin or the | thin → thin, the → thu |
| v | v as in van | van → van |
| w | w as in win | win → win |
| y | y as in yes | yes → yes |
| z | z as in zoo | zoo → zoo |
| zj | zh as in measure | measure → mezjyr |

notable differences from english:

- **k replaces c** for the /k/ sound — cat → kat, cake → kaek
- **g is always hard** — there is no soft g (that sound is spelled j)
- **th covers both th sounds** — thin (voiceless θ) and the (voiced ð) both use `th`
- **zj is new** — english has no dedicated spelling for the sound in measure, pleasure, vision

## vowels

vowels follow three simple rules based on what's next to them.

### rule 1: a vowel by itself makes its short sound

when a vowel appears alone (not next to another vowel), it makes its common short sound.

| inglish | sound | english examples |
|----------|-------|-----------------|
| a | a as in cat | cat → kat, bat → bat |
| e | e as in bet | bet → bet, pen → pen |
| i | i as in bit | bit → bit, fish → fish |
| o | o as in dog | dog → dog, for → for, law → laa |
| u | u as in but, or the schwa sound | but → but, about → ubout |

the schwa (the unstressed "uh" sound in words like about, the, mother) is spelled `u` because it sounds closest to short u.

### rule 2: a vowel followed by `e` sounds like its name

adding `e` immediately after a vowel makes it "say its name" — the long vowel sound.

| inglish | sound | english examples |
|----------|-------|-----------------|
| ae | long a as in make | make → maek, cake → kaek |
| ee | long e as in see | see → see, meet → meet, seat → seet |
| ie | long i as in bike | bike → biek, time → tiem, night → niet |
| oe | long o as in go | go → goe, home → hoem, phone → foen |
| ue | long u as in use | use → ues, cute → kuet |

this replaces english's unpredictable "silent e" rule with a consistent vowel pair.

### rule 3: a doubled vowel makes an elongated sound

repeating a vowel produces a longer, distinct vowel sound.

| inglish | sound | english examples |
|----------|-------|-----------------|
| aa | ah as in hot | hot → haat, pot → paat, rock → raak |
| oo | oo as in food | food → food, through → throo, blue → bloo |
| uu | oo as in book | book → buuk, put → puut, push → puush |

### diphthongs and r-colored vowels

a few vowel combinations represent sounds that glide between two vowels, plus one r-colored vowel.

| inglish | sound | english examples |
|----------|-------|-----------------|
| ou | ou as in out | out → out, loud → loud |
| oi | oi as in boy | boy → boi, coin → koin |
| yr | ur as in bird | bird → byrd, her → hyr, turn → tyrn, world → wyrld |

## reading rule: first diphthong wins

when two vowels are adjacent, read left to right and match the first diphthong or digraph you find. this resolves cases where separate vowel sounds happen to sit next to each other.

for example, `ukrooul` (accrual) contains `ou` — but reading left to right, `oo` matches first, leaving a lone `u`. the word reads as `u-k-r-oo-u-l`, not `u-k-r-o-ou-l`.

more examples:

| inglish | greedy parse | sounds |
|----------|-------------|--------|
| ukrooul (accrual) | u-k-r-**oo**-u-l | /ʌ-k-ɹ-uː-ʌ-l/ |
| ukrooing (accruing) | u-k-r-**oo**-i-ng | /ʌ-k-ɹ-uː-ɪ-ŋ/ |
| looes (laos) | l-**oo**-e-s | /l-uː-ɛ-s/ |
| aeemae (AMA) | **ae**-e-m-**ae** | /eɪ-ɛ-m-eɪ/ |

this rule eliminates nearly all ambiguity from the vowel system — without it, `oo` + `i` could be misread as `o` + `oi`.

## alternate pronunciations

when a word has more than one accepted pronunciation, use the one whose inglish spelling is closest to the current US english spelling. this keeps inglish as readable as possible for english speakers.

for example, "hello" has two pronunciations:

| pronunciation | IPA | inglish | distance from english |
|--------------|-----|----------|----------------------|
| heh-LOW | /hɛloʊ/ | heloe | close — `hel` matches |
| huh-LOW | /hʌloʊ/ | huloe | further — `hul` doesn't match |

`heloe` wins because it preserves more of the original english spelling.

## summary

the entire system rests on a few principles:

1. **every letter or letter combination has exactly one sound**
2. **letter-to-sound assignments stay close to standard english**
3. **vowel sounds change only based on the immediately adjacent vowel:**
   - vowel alone → short sound
   - vowel + e → long sound (name of the vowel)
   - vowel + same vowel → elongated sound
4. **first diphthong wins** — read left to right, match the first vowel pair
5. **no silent letters** — every letter you see, you pronounce
6. **no exceptions** — the rules apply to every word
