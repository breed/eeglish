# deploying the inglish MCP server to a VPS

serves the MCP server publicly at `https://mcp.inglish.us/mcp` (streamable HTTP,
no auth — it's a read-only dictionary). stdio stays the default transport for
local use; nothing about local registrations changes.

## architecture

```
client ──https──> nginx (TLS, rate limit, Host check) ──> 127.0.0.1:8000 inglish-mcp --http
```

the python server binds only to localhost; nginx terminates TLS and is the only
public listener. the server is installed from PyPI (package `inglish`), which
bundles the dictionary, rules, and alphabet — no repo checkout needed.

## steps

1. **DNS** — add an `A` record for `mcp.inglish.us` pointing at the VPS IP
   (at your registrar; inglish.us apex stays on github pages, this is a new
   subdomain).

2. **install from PyPI** — on the VPS:

   ```
   sudo apt install python3-venv
   sudo python3 -m venv /opt/inglish/venv
   sudo /opt/inglish/venv/bin/pip install inglish
   sudo useradd --system --no-create-home inglish
   ```

3. **service** —

   ```
   sudo cp deploy/inglish-mcp.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable --now inglish-mcp
   ```

   check: `curl -s http://127.0.0.1:8000/mcp` should answer (a 4xx JSON-RPC
   complaint is fine — it means the server is up).

4. **nginx + TLS** —

   ```
   sudo apt install nginx certbot python3-certbot-nginx
   sudo cp deploy/nginx-mcp.conf /etc/nginx/sites-available/inglish-mcp
   sudo ln -s /etc/nginx/sites-available/inglish-mcp /etc/nginx/sites-enabled/
   sudo nginx -t && sudo systemctl reload nginx
   sudo certbot --nginx -d mcp.inglish.us
   ```

5. **verify from anywhere** —

   ```
   claude mcp add --transport http inglish-remote https://mcp.inglish.us/mcp
   ```

   then ask claude to translate something.

## updating

the dictionary, rules, and alphabet ship inside the PyPI package, so an update
is: publish a new `inglish` release, then on the VPS:

```
sudo /opt/inglish/venv/bin/pip install -U inglish
sudo systemctl restart inglish-mcp
```

## security posture

- python process binds 127.0.0.1 only; nginx is the sole public surface
- TLS via certbot; plain-http requests get redirected by certbot's config
- rate limit: 10 req/s per IP (burst 20) in nginx
- default_server block returns 444 to wrong-Host requests (DNS-rebinding guard)
- systemd unit runs as an unprivileged system user with a read-only filesystem
  view (`ProtectSystem=strict`, `ReadOnlyPaths=/opt/inglish`)
- the server itself is read-only by construction: no writes, no subprocesses,
  no outbound network (see the security review notes in the repo history)
