# changelog

## 0.1.0 (2026-07-02)

first release.

- `inglish` CLI: translate english text to inglish spelling (files or stdin)
- `inglish-mcp` MCP server: `translate`, `lookup_word`, `reverse_translate`
  tools plus `inglish://rules` and `inglish://alphabet` resources
- transports: stdio (default) and stateless streamable HTTP (`--http`) for
  remote hosting behind a TLS proxy
- ships the full 125,857-word dictionary (`dikshuneree.json`), spelling rules
  (`RULES.md`), and alphabet (`ALFUBET.md`)
