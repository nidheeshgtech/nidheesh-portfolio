"""Build the deploy folder (dist/) for Cloudflare Pages.

  python3 tools/build_dist.py

Reads site.config.json (site_url, gtm_id). Copies only what the live site needs, rewrites internal links
to clean URLs (/work/ai71), adds canonical + absolute social-image URLs, the GTM snippet, sitemap.xml,
robots.txt, _headers and _redirects, and minifies CSS/JS (esbuild via npx when available)."""
import os, re, json, shutil, subprocess, datetime, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
os.chdir(ROOT)
cfg = json.load(open('site.config.json'))
SITE = cfg['site_url'].rstrip('/')
GTM = cfg.get('gtm_id', '').strip()
GA4 = '' if GTM else cfg.get('ga4_id', '').strip()          # with GTM, set GA4 up inside the container instead
GSV = cfg.get('google_site_verification', '').strip()
for k, v, pat in (('gtm_id', GTM, r'GTM-[A-Z0-9]+'), ('ga4_id', GA4, r'G-[A-Z0-9]+')):
    if v and not re.fullmatch(pat, v):
        raise SystemExit(f'site.config.json: {k} "{v}" does not look like {pat}')
DIST = os.path.join(ROOT, 'dist')
TODAY = datetime.date.today().isoformat()

if os.path.isdir(DIST):
    shutil.rmtree(DIST)
os.makedirs(DIST)

# ---------- files that go live ----------
COPY = ['favicon.svg', 'favicon.ico', 'favicon-32.png', 'apple-touch-icon.png', 'site.webmanifest',
        'assets/fonts', 'assets/js/vendor', 'assets/img/og.jpg', 'assets/img/og', 'assets/img/icon-192.png', 'assets/img/icon-512.png',
        'assets/img/me/portrait-back.webp', 'assets/img/me/portrait-back-760.webp']
pages = ['index.html', '404.html'] + sorted(glob.glob('work/*.html'))

# images actually referenced by the pages (skips unused screenshots and old portraits)
used = set()
for p in pages:
    for ref in re.findall(r'(?:src|href|srcset|imagesrcset)="([^"]+)"', open(p).read()):
        for part in ref.split(','):
            u = part.strip().split(' ')[0].split('?')[0]
            u = re.sub(r'^(\.\./|/)', '', u)
            if u.startswith('assets/img/') and os.path.isfile(u):
                used.add(u)
for item in COPY + sorted(used):
    src, dst = os.path.join(ROOT, item), os.path.join(DIST, item)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    (shutil.copytree if os.path.isdir(src) else shutil.copy2)(src, dst)

# ---------- CSS / JS (minified) ----------
os.makedirs(os.path.join(DIST, 'assets/css'), exist_ok=True)
os.makedirs(os.path.join(DIST, 'assets/js'), exist_ok=True)
def minify(src, dst, loader):
    try:
        r = subprocess.run(['npx', '--yes', 'esbuild@0.24.0', src, '--minify', '--target=es2019,safari14', f'--outfile={dst}', '--log-level=error'],
                           capture_output=True, text=True, timeout=180)
        if r.returncode == 0 and os.path.getsize(dst) > 0:
            return 'esbuild'
    except Exception:
        pass
    shutil.copy2(src, dst)
    return 'copied (esbuild unavailable)'
m1 = minify('assets/css/style.css', os.path.join(DIST, 'assets/css/style.css'), 'css')
m2 = minify('assets/js/main.js', os.path.join(DIST, 'assets/js/main.js'), 'js')

# ---------- pages ----------
GTM_HEAD = f'''  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{GTM}');</script>
''' if GTM else ''
GTM_BODY = f'''  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM}" height="0" width="0" style="display:none;visibility:hidden" title="Google Tag Manager"></iframe></noscript>
''' if GTM else ''
GA4_HEAD = f'''  <!-- Google Analytics 4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA4}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA4}');</script>
''' if GA4 else ''
GSV_META = f'  <meta name="google-site-verification" content="{GSV}">\n' if GSV else ''

def clean_url(path):
    """work/ai71.html -> /work/ai71 ; index.html -> /"""
    path = path.replace('index.html', '')
    return '/' + re.sub(r'\.html$', '', path)

sitemap = []
for p in pages:
    h = open(p).read()
    url_path = clean_url(p)
    canonical = SITE + (url_path if url_path != '/' else '/')
    depth = p.count('/')
    # internal links -> clean, root-absolute URLs
    if depth:  # work/*.html
        h = re.sub(r'href="\.\./index\.html(#[^"]*)?"', lambda m: f'href="/{m.group(1) or ""}"', h)
        h = re.sub(r'href="([a-z0-9-]+)\.html"', r'href="/work/\1"', h)
    else:
        h = re.sub(r'href="work/([a-z0-9-]+)\.html"', r'href="/work/\1"', h)
    # absolute social image + site URL placeholders
    h = re.sub(r'content="(?:\.\./|/)?(assets/img/og[^"]*\.jpg)"', lambda m: f'content="{SITE}/{m.group(1)}"', h)
    h = h.replace('{{SITE_URL}}', SITE)
    if p != '404.html':
        h = h.replace('  <meta property="og:type"', f'  <link rel="canonical" href="{canonical}">\n  <meta property="og:url" content="{canonical}">\n  <meta property="og:type"', 1)
        sitemap.append((canonical, '1.0' if p == 'index.html' else '0.7'))
    if p == 'index.html':
        h = h.replace('<meta property="og:type" content="website">', '<meta property="og:type" content="profile">', 1)
    if GTM:
        h = h.replace('<head>\n', '<head>\n' + GTM_HEAD, 1)
        h = h.replace('<body>\n', '<body>\n' + GTM_BODY, 1)
    elif GA4:
        h = h.replace('<head>\n', '<head>\n' + GA4_HEAD, 1)
    if GSV and p == 'index.html':
        h = h.replace('  <meta name="author"', GSV_META + '  <meta name="author"', 1)
    out = os.path.join(DIST, p)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(h)

# ---------- SEO + Cloudflare files ----------
open(os.path.join(DIST, 'sitemap.xml'), 'w').write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    ''.join(f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n' for u, pr in sitemap) + '</urlset>\n')
open(os.path.join(DIST, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')

csp = ("default-src 'self'; "
       "script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://*.googletagmanager.com https://www.google-analytics.com https://*.google-analytics.com; "
       "connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com https://*.googletagmanager.com https://www.google.com; "
       "img-src 'self' data: https://*.google-analytics.com https://*.googletagmanager.com https://www.google.com https://www.google.ae; "
       "style-src 'self' 'unsafe-inline' https://www.googletagmanager.com; "
       "font-src 'self'; frame-src https://www.googletagmanager.com; "
       "frame-ancestors 'none'; base-uri 'self'; form-action 'self'; object-src 'none'; upgrade-insecure-requests")
open(os.path.join(DIST, '_headers'), 'w').write(f'''/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()
  X-Frame-Options: DENY
  Cross-Origin-Opener-Policy: same-origin
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: {csp}

/assets/fonts/*
  Cache-Control: public, max-age=31536000, immutable
  Access-Control-Allow-Origin: *

/assets/css/*
  Cache-Control: public, max-age=31536000, immutable

/assets/js/*
  Cache-Control: public, max-age=31536000, immutable

/assets/img/*
  Cache-Control: public, max-age=2592000, stale-while-revalidate=86400

/*.html
  Cache-Control: public, max-age=0, must-revalidate

/
  Cache-Control: public, max-age=0, must-revalidate
''')
open(os.path.join(DIST, '_redirects'), 'w').write('/index /  301\n/home /  301\n/work /#work 302\n/contact /#contact 302\n')

# ---------- report ----------
size = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(DIST) for f in fs)
files = sum(len(fs) for _, _, fs in os.walk(DIST))
print(f'dist/ ready: {files} files, {size / 1024 / 1024:.2f} MB | css {m1}, js {m2} | tracking {"GTM " + GTM if GTM else ("GA4 " + GA4 if GA4 else "off")} | site {SITE}')
if 'example.com' in SITE:
    print('NOTE: site_url is still example.com. Set your domain in site.config.json and build again before publishing.')
