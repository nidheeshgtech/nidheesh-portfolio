"""Font preview pages: copies of index.html with a different Google font pairing.
Writes font-<name>.html next to index.html (not part of the deploy). Run after tools/pages.py."""
import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

HEADINGS = ('.wordmark, .hero__title, .statement, .project__name, .more__name, .service h3, '
            '.about__lead, .faq__title, .talk__title, .tile__value, .case-title, .case-next__name')
VARIANTS = [
    ('current', 'Current: Schibsted Grotesk', None, ''),
    ('bricolage', 'Bricolage Grotesque',
     'family=Bricolage+Grotesque:opsz,wght@12..96,400..800&family=JetBrains+Mono:wght@500',
     ':root{--sans:"Bricolage Grotesque",Arial,sans-serif;--mono:"JetBrains Mono",ui-monospace,monospace}'
     '.wordmark{letter-spacing:-.065em;font-weight:800}'),
    ('funnel', 'Funnel Display + Funnel Sans',
     'family=Funnel+Display:wght@400..800&family=Funnel+Sans:wght@400..700&family=DM+Mono:wght@500',
     ':root{--sans:"Funnel Sans",Arial,sans-serif;--mono:"DM Mono",ui-monospace,monospace}'
     + HEADINGS + '{font-family:"Funnel Display","Funnel Sans",Arial,sans-serif}'
     '.wordmark{letter-spacing:-.06em;font-weight:800}'),
    ('instrument', 'Instrument Sans (condensed headlines)',
     'family=Instrument+Sans:wdth,wght@75..100,400..700&family=Space+Mono',
     ':root{--sans:"Instrument Sans",Arial,sans-serif;--mono:"Space Mono",ui-monospace,monospace}'
     + HEADINGS + '{font-stretch:78%}'
     '.wordmark{letter-spacing:-.04em;font-weight:700;font-stretch:75%}.hero__title{letter-spacing:-.035em}'),
]

src = open('index.html').read()
for name, label, gf, css in VARIANTS:
    links = ''.join(f'<a href="{"index" if n == "current" else "font-" + n}.html"{" aria-current=\"page\"" if n == name else ""}>{l.split(":")[-1].split("(")[0].strip()}</a>'
                    for n, l, _, _ in VARIANTS)
    switcher = ('<nav class="font-switch" aria-label="Font versions"><span>Font</span>' + links + '</nav>'
                '<style>.font-switch{position:fixed;left:16px;bottom:16px;z-index:99;display:flex;gap:4px;align-items:center;'
                'padding:6px;background:#171717;color:#f0f0ef;border-radius:4px;font:500 13px/1 system-ui,sans-serif;box-shadow:0 6px 24px rgba(0,0,0,.2)}'
                '.font-switch span{padding:0 8px;opacity:.6}.font-switch a{color:inherit;text-decoration:none;padding:7px 10px;border-radius:3px}'
                '.font-switch a:hover{background:#333}.font-switch a[aria-current]{background:#f0f0ef;color:#171717}</style>')
    if name == 'current':
        continue
    page = src.replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
    head_add = (f'  <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
                f'  <link href="https://fonts.googleapis.com/css2?{gf}&display=swap" rel="stylesheet">\n'
                f'  <style>{css}</style>\n')
    page = page.replace('</head>', head_add + '</head>', 1)
    page = page.replace('</body>', switcher + '\n</body>', 1)
    page = page.replace('<title>', f'<title>[{label}] ', 1)
    open(f'font-{name}.html', 'w').write(page)
    print('wrote', f'font-{name}.html')
