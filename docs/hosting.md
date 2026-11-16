# Hosting

The page is static: any web server works. The projector loads it once per boot and keeps the photos in its
browser storage (IndexedDB), so it only re-downloads photos that changed.

## Cloudflare Pages, public but unlisted (required)

This project publishes only to Cloudflare Pages. Account setup for beginners: the README section
**Cloudflare account (required)**. Publishing: `./deploy-cloudflare.sh` (needs Node; `wrangler login` opens a
browser once, where you select **Allow**).

- Everything lives under `/<32 random hex chars>/`; the root and all other paths are 404.
- `noindex` headers, `robots.txt` disallow, `Referrer-Policy: no-referrer`, a strict Content-Security-Policy.
- A 6-letter short link (`/<code>`) redirects to the wall, because typing 32 characters with a TV remote is
  miserable. It is guessable with effort; delete those `_redirects` lines in the script if that matters.
- **Anyone with the full URL can see the photos.** Don't post it, and treat `.cloudflare-site` as a secret.
- The script deploys to the production branch (`main`), so the address is `https://<project>.pages.dev`,
  public by default. Nothing needs enabling in the dashboard. The Pages setting **Settings → General → Access
  policy** only covers preview deployments; leave it off.
- Free tier limits are far above what a photo wall needs (files up to 25 MB, 20,000 files, 500 deploys a month).

Want a login instead? Put Cloudflare Access (Zero Trust, free for small teams) in front of the project. The
kiosk then has to log in once and keep the cookie, and some kiosk browsers lose it, so this is for advanced
users only.

## Troubleshooting

| Problem | Fix |
|---|---|
| The browser tab for `wrangler login` never opened | run `npx -y wrangler@4.158.0 login` yourself, select **Allow**, then re-run `./deploy-cloudflare.sh` |
| "Authentication error" or "not authorized" | the login expired or went to another account: `npx -y wrangler@4.158.0 logout`, then re-run the script and allow again with the right account |
| An error mentioning email verification | open the verification email from Cloudflare (check spam), click the link, re-run the script |
| Asked to choose an account | pick the one you created for the wall; to skip the question next time, run `export CLOUDFLARE_ACCOUNT_ID=<id>` (shown in the dashboard's account home URL) |
| "This site can't be reached" right after the first deploy | a new `pages.dev` address can take a few minutes to appear; wait and retry |
| `photowall-….pages.dev` says "Not found" | expected: only the short link and the wall path work |
| A Cloudflare login screen instead of the wall | a Zero Trust Access application covers the address: remove it under **Zero Trust → Access → Applications** |
| The wall shows old photos | re-run `./deploy-cloudflare.sh`; the projector picks up changes on its next page load |

Don't move the wall to GitHub Pages or any host that serves from a public repository: the photos would be
public in git history.
