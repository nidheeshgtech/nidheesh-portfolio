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

## Google tracking
Set in `site.config.json`, then push (Vercel rebuilds):
- `ga4_id`: `G-XXXXXXXXXX`. Loads GA4 directly; the events below are sent as GA4 events.
- or `gtm_id`: `GTM-XXXXXXX`. Loads Tag Manager instead (ga4_id is then ignored; add the GA4 tag inside GTM). Events arrive as dataLayer pushes.
- `google_site_verification`: the `content` value from Search Console's HTML tag method (added to the home page only).

| event | params |
|---|---|
| `contact_click` | `contact_method` (email, linkedin), `link_location` |
| `email_copy` | `link_location` |
| `case_study_click` | `project`, `link_location` |
| `outbound_click` | `link_url`, `link_location` |
| `faq_open` | `question` |
| `section_view` | `section` (work, services, about, contact) |

In GA4: Admin > Custom definitions > add event-scoped dimensions `contact_method`, `link_location`, `project`, `section`, `question`;
Admin > Key events > mark `contact_click` and `email_copy`. CSP (vercel.json / _headers) already allows Google's domains.
