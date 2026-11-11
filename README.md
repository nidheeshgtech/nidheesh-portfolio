# Nidheesh Narayanan — portfolio

Static site (HTML/CSS/JS). Local preview in MAMP: http://localhost:8888/nidheesh-portfolio-2026/

## Publish (Cloudflare Pages)
1. Edit `site.config.json`: `site_url` = your domain (e.g. `https://nidheesh.dev`), `gtm_id` = `GTM-XXXXXXX`.
2. `python3 tools/build_dist.py` → writes `dist/` (only live files, minified, canonical URLs, sitemap, robots, headers, GTM).
3. Upload `dist/` in Cloudflare Pages (Direct Upload), or `npx wrangler pages deploy dist`.
4. Add the custom domain in Pages → Custom domains. In Cloudflare: SSL "Full (strict)", Always Use HTTPS on.
5. Google Search Console: add the domain, submit `https://YOUR-DOMAIN/sitemap.xml`.
6. Check the share card: https://www.opengraph.xyz (uses `assets/img/og.jpg`).

Preview the build like Cloudflare does (clean URLs, 404, headers): `python3 tools/serve_dist.py` → http://localhost:8790

## Editing
- Page shell/content: `tools/pages.py` → regenerates `index.html`, `work/*.html` (keeps each case page's `<main>`), `404.html`.
- Styles `assets/css/style.css`, scripts `assets/js/main.js`. Social image + icons: `tools/make_icons.py`.
- Font previews (not deployed): `font-bricolage.html`, `font-funnel.html`, `font-instrument.html` — `tools/font_variants.py`.
- Case pages still need your own paragraph on role, challenges and results (none were invented).

## GTM / dataLayer events (pushed by main.js)
| event | params |
|---|---|
| `contact_click` | `contact_method` (email, phone, whatsapp, linkedin), `link_location` |
| `email_copy` | `link_location` |
| `case_study_click` | `project`, `link_location` |
| `outbound_click` | `link_url`, `link_location` |
| `faq_open` | `question` |
| `section_view` | `section` (work, services, about, contact) |

In GTM: add a GA4 Configuration tag (All Pages), then Custom Event triggers for the events above with GA4 Event tags,
Data Layer Variables for the params, and mark `contact_click` + `email_copy` as key events in GA4.
CSP in `_headers` already allows GTM + GA4; if you add other vendors (Hotjar, Clarity…) add their domains there.
