# Hosting

The page is static: any web server works. The projector loads it once per boot and keeps the photos in its
browser storage (IndexedDB), so it only re-downloads photos that changed.

## Cloudflare Pages, public but unlisted (default)

`./deploy-cloudflare.sh` (needs Node and a free Cloudflare account; `wrangler login` opens a browser once).

- Everything lives under `/<32 random hex chars>/`; the root and all other paths are 404.
- `noindex` headers, `robots.txt` disallow, `Referrer-Policy: no-referrer`, a strict Content-Security-Policy.
- A 6-letter short link (`/<code>`) redirects to the wall, because typing 32 characters with a TV remote is
  miserable. It is guessable with effort; delete those `_redirects` lines in the script if that matters.
- **Anyone with the full URL can see the photos.** Don't post it, and treat `.cloudflare-site` as a secret.
- Free tier limits are far above what a photo wall needs (files up to 25 MB, 20,000 files).

Want a login instead? Put Cloudflare Access (Zero Trust, free for small teams) in front of the project. Note
the kiosk then needs to log in once and keep the cookie.

## Local network only (nothing leaves your home)

Run the site on an always-on computer (or a Raspberry Pi / NAS) in the house:

```bash
./serve.sh 8000          # serves site/ on port 8000
```

Fully Kiosk's start URL becomes `http://<that computer's LAN IP>:8000/#play`. Give that computer a fixed IP in
your router. The server must be running whenever the projector boots. Audio autoplay rules are the same.

## Other static hosts

Netlify honours the same `_headers`/`_redirects` files (copy `build/cloudflare/` after
`./deploy-cloudflare.sh --dry-run`). **Don't use GitHub Pages from a public repo**: the photos would be in a
public repository.
