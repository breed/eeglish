#!/usr/bin/env python3
"""inglish_mcp - serve the inglish translator over the Model Context Protocol."""

import argparse

from mcp.server.fastmcp import FastMCP

from tranzlaet import data_path, load_dictionary, translate_text

DICTIONARY = load_dictionary()           # english -> inglish (lowercased keys)

# reverse index: inglish spelling -> [english, ...] (collisions are real)
REVERSE = {}
for eng, ing in DICTIONARY.items():
    REVERSE.setdefault(ing.lower(), []).append(eng)

mcp = FastMCP("inglish")


def _norm(word):
    # mirror translate_text's normalization: lowercase + curly->ascii apostrophe
    return word.strip().lower().replace("’", "'")


@mcp.tool()
def translate(text: str) -> str:
    """Translate english text to inglish spelling, preserving capitalization,
    punctuation, contractions, and HTML tags."""
    return translate_text(text, DICTIONARY)


@mcp.tool()
def lookup_word(word: str) -> dict:
    """Look up the inglish spelling of a single english word."""
    key = _norm(word)
    inglish = DICTIONARY.get(key)
    return {"english": key, "inglish": inglish, "found": inglish is not None}


@mcp.tool()
def reverse_translate(spelling: str) -> dict:
    """Given an inglish spelling, return every english word that maps to it.

    Reverse translation is lossy — multiple english words can share one
    inglish spelling — so all candidates are returned.
    """
    key = _norm(spelling)
    return {"inglish": key, "candidates": REVERSE.get(key, [])}


def _read(name):
    with open(data_path(name), encoding="utf-8") as f:
        return f.read()


@mcp.resource("inglish://rules")
def rules() -> str:
    """The complete inglish spelling rules (RULES.md)."""
    return _read("RULES.md")


@mcp.resource("inglish://alphabet")
def alphabet() -> str:
    """The IPA-to-inglish letter mapping (ALFUBET.md)."""
    return _read("ALFUBET.md")


def main():
    parser = argparse.ArgumentParser(
        description="Serve the inglish translator over the Model Context Protocol."
    )
    parser.add_argument(
        "--http",
        action="store_true",
        help="serve streamable HTTP at /mcp instead of stdio",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="HTTP bind address (default: 127.0.0.1; put a TLS proxy in front)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="HTTP port (default: 8000)",
    )
    args = parser.parse_args()

    if args.http:
        mcp.settings.host = args.host
        mcp.settings.port = args.port
        # tools are pure lookups, so run stateless: no per-session state,
        # requests survive restarts and need no session pinning behind a proxy
        mcp.settings.stateless_http = True
        mcp.run(transport="streamable-http")
    else:
        mcp.run()  # stdio transport


if __name__ == "__main__":
    main()
