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
- `DIKSHUNEREE.md` - 125,857 word dictionary with columns `english`, `inglish`, `IPA`
- `dikshuneree.json` - JSON version of the dictionary for the website
- `generate_dictionary.py` - regenerates `DIKSHUNEREE.md` and `dikshuneree.json` from CMU Pronouncing Dictionary
- `tranzlaet.py` - CLI tool that translates english text to inglish (`python3 tranzlaet.py [file...]` or stdin)
- `test_tranzlaet.py` - unit tests for tranzlaet.py (`python3 -m unittest test_tranzlaet`)
- `inglish_mcp.py` - MCP server exposing the translator to LLM clients over stdio (`translate`, `lookup_word`, `reverse_translate` tools; `RULES.md`/`ALFUBET.md` resources)
- `test_inglish_mcp.py` - unit tests for inglish_mcp.py (`python3 -m unittest test_inglish_mcp`)
- `requirements.txt` - runtime deps for the MCP server (`mcp`)
- `deploy/` - VPS deployment for the remote MCP endpoint (systemd unit, nginx config, step-by-step README)
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
5. excludes acronyms (words whose only pronunciations are letter-by-letter spellings), plus a manual exclusion list for acronym-dominant words that escape the filter via a real-word pronunciation (ai)
6. preserves contractions: translates the base word, keeps the apostrophe and suffix ('t, 's, 'd, 'm, 'l, 'r, 'v)
7. skips leading-apostrophe words ('em, 'twas, etc.) — they pass through the translator unchanged
8. words ending in a bare apostrophe (plural possessives like lawyers', dropped-letter words like goin' and ol') keep the trailing apostrophe in the inglish spelling

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
- curly apostrophes (’) are normalized to ' for dictionary lookup, and restored in the translated output
- the tokenizer regex is `<[^>]*>|[^<\s]+|<|\s+` — splits on whitespace and HTML tags; a lone `<` with no closing `>` passes through as its own token
- the punctuation regex `^([^\w]*)(\w.*\w|\w)([^\w]*)$` strips leading/trailing non-word characters before dictionary lookup
- if the stripped trailing punctuation starts with an apostrophe, the apostrophe-inclusive dictionary key is tried first so trailing-apostrophe entries (lawyers', goin', ol') are reachable
- the JS translators check dictionary words with `Object.prototype.hasOwnProperty` so prototype names (e.g. __proto__) in the text never false-match
- a single capital letter is treated as title case, not ALL CAPS (I → Ie)
- `test_tranzlaet.py` covers the python translator (`python3 -m unittest test_tranzlaet`)

## mcp server

`inglish_mcp.py` serves the translator over the Model Context Protocol (stdio) so LLM clients (Claude Desktop, Claude Code, etc.) can call it. it imports `translate_text` from `tranzlaet.py` and loads `dikshuneree.json` once at startup — no translation logic is duplicated.

- built on the official python `mcp` SDK (FastMCP); the only runtime dep, pinned in `requirements.txt`
- tools:
  - `translate(text)` — full text → inglish, reusing `translate_text` (preserves caps, punctuation, contractions, HTML)
  - `lookup_word(word)` — single english word → `{english, inglish, found}` (no IPA)
  - `reverse_translate(spelling)` — inglish → `{inglish, candidates}`; returns **all** english words for that spelling (reverse is lossy, so a reverse index of inglish → [english, …] is built once at startup)
- resources: `inglish://rules` (RULES.md) and `inglish://alphabet` (ALFUBET.md), read per-request so they always reflect the current files
- install + run: `venv/bin/pip install -r requirements.txt`, then `venv/bin/python3 inglish_mcp.py`
- register with claude code: `claude mcp add inglish -- /home/bcr33d/git/inglish/venv/bin/python3 /home/bcr33d/git/inglish/inglish_mcp.py`
- transports: stdio by default; `--http [--host H] [--port P]` serves stateless streamable HTTP at `/mcp` (binds 127.0.0.1, meant to sit behind a TLS reverse proxy)
- remote deployment (mcp.inglish.us on a VPS): see `deploy/README.md` — nginx terminates TLS, rate-limits, and Host-checks; systemd runs the server as an unprivileged user; register with `claude mcp add --transport http inglish https://mcp.inglish.us/mcp`
- `test_inglish_mcp.py` covers the three tools (`python3 -m unittest test_inglish_mcp`)
- if a translation rule or the dictionary changes, the server needs no edits — it reads `dikshuneree.json` and reuses `translate_text` live

## website rules tab

the rules tab in `index.html` fetches `RULES.md` at runtime and renders it to HTML using a simple inline markdown parser. this means the rules tab is always in sync with `RULES.md` — no manual HTML updates needed.

the markdown parser handles: headings, tables, bold, code, links, ordered/numbered lists (with nested sub-bullets), and paragraphs. if new markdown features are added to `RULES.md` (e.g. blockquotes, images), the parser in `index.html` may need to be extended.

the parser HTML-escapes all text before rendering (so literal `<`, `>`, `&` in RULES.md display correctly) and only allows http(s), mailto, and relative link targets.
