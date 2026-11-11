"""Page generator: writes index.html and the shell of every work/*.html page (their <main> is kept).
Run from anywhere:  python3 tools/pages.py      then build the deploy folder with  python3 tools/build_dist.py"""
import os, re, html, time
ASSET_V = time.strftime('%Y%m%d%H%M')
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

ARROW = '<svg viewBox="0 0 14 14" aria-hidden="true"><path d="M3.5 10.5 10.5 3.5M5 3.5h5.5V9" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
EMAIL = 'hello.nidheesh@gmail.com'
LINKEDIN = 'https://www.linkedin.com/in/nidheesh-narayanan-b9180853/'

# slug, name, sector, languages, platform, host
P = [
    ('quantumgate', 'QuantumGate', 'Cybersecurity', 'English', 'WordPress', 'quantumgate.ae'),
    ('ai71', 'AI71', 'AI platform', 'English and Arabic', 'Frontend', 'ai71.ai'),
    ('dwe', 'Dubai Women Establishment', 'Government', 'English and Arabic', 'WordPress, Elementor', 'dwe.gov.ae'),
    ('boatshow', 'Dubai International Boat Show', 'Exhibition', 'English', 'WordPress', 'boatshowdubai.com'),
    ('wps', 'World Police Summit', 'Government summit', 'English and Arabic', 'WordPress', 'worldpolicesummit.com'),
    ('gulfood', 'Gulfood Manufacturing', 'Trade exhibition', 'English', 'WordPress', 'gulfoodmanufacturing.com'),
    ('ducab', 'Ducab', 'Manufacturing', 'English and Arabic', 'WordPress', 'ducab.com'),
    ('gbc', 'UAE Gender Balance Council', 'Government', 'English and Arabic', 'WordPress', 'gbc.gov.ae'),
    ('futurehealth', 'Future Health Initiative', 'Healthcare', 'English', 'WordPress', 'futurehealthinitiative.ae'),
    ('payfuture', 'PayFuture', 'Payments', 'English', 'WordPress, Elementor', 'payfuture.net'),
    ('mbzuai', 'MBZUAI', 'Education and research', 'English and Arabic', 'Frontend', 'mbzuai.ac.ae'),
]
# government work gets a badge (Ducab is owned by the Dubai and Abu Dhabi governments, so it says so)
GOV = {'dwe': 'Government', 'wps': 'Government', 'gbc': 'Government', 'ducab': 'Government-owned'}
SHIELD = '<svg viewBox="0 0 14 14" aria-hidden="true"><path d="M7 1.2 2.4 3v3.7c0 2.8 1.9 5 4.6 5.9 2.7-.9 4.6-3.1 4.6-5.9V3z" fill="currentColor"/></svg>'
def badge(slug, cls='gov-badge'):
    return f'<span class="{cls}">{SHIELD}{GOV[slug]}</span>' if slug in GOV else ''

intro = {}
for slug, *_ in P:
    m = re.search(r'<p class="case-intro">([^<]*)', open(f'work/{slug}.html').read())
    intro[slug] = m.group(1)

KEYWORDS = 'Nidheesh Narayanan, frontend developer Dubai, React developer Dubai, Next.js developer, WordPress developer Dubai, Arabic RTL websites, bilingual websites UAE, government websites UAE, web accessibility, WCAG'

def head(title, desc, prefix, extra='', og='og.jpg', og_alt='Nidheesh Narayanan, senior frontend developer in Dubai: React, Next.js and WordPress'):
    return f'''<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script>(function(d){{var r=d.documentElement;r.className=r.className.replace('no-js','js');try{{var f=/[?&]loader(=|&|$)/.test(location.search);if(f||(!sessionStorage.getItem('nn-seen')&&!matchMedia('(prefers-reduced-motion: reduce)').matches))r.className+=' has-loader';}}catch(e){{}}}})(document);</script>
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="author" content="Nidheesh Narayanan">
  <meta name="keywords" content="{KEYWORDS}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="theme-color" content="#ececeb">
  <meta name="format-detection" content="telephone=no">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Nidheesh Narayanan">
  <meta property="og:locale" content="en_AE">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{prefix}assets/img/{og}">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{og_alt}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{prefix}assets/img/{og}">
  <meta name="twitter:image:alt" content="{og_alt}">
  <link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml">
  <link rel="icon" href="{prefix}favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="{prefix}apple-touch-icon.png">
  <link rel="manifest" href="{prefix}site.webmanifest">
  <link rel="preload" href="{prefix}assets/fonts/schibsted-grotesk-latin.woff2" as="font" type="font/woff2" crossorigin>
{extra}  <link rel="stylesheet" href="{prefix}assets/css/style.css?v={ASSET_V}">
'''

def header(home, prefix):
    nav = ''.join(f'\n        <a href="{home}#{i}">{t}</a>' for i, t in [('work', 'Work'), ('services', 'Services'), ('about', 'About')])
    mnav = ''.join(f'\n      <a href="{home}#{i}">{t}</a>' for i, t in [('work', 'Work'), ('services', 'Services'), ('about', 'About'), ('contact', 'Contact')])
    return f'''<body>
  <div class="loader" aria-hidden="true">
    <svg class="loader__n" viewBox="0 0 120 132">
      <defs><clipPath id="loader-clip"><rect x="22" y="20" width="76" height="91"/></clipPath></defs>
      <g clip-path="url(#loader-clip)">
        <path class="loader__track" d="M26.9 9.7L93.1 121.3"/>
        <path class="loader__arc" d="M26.9 9.7L93.1 121.3" pathLength="100"/>
      </g>
      <rect class="loader__leg" x="22" y="20" width="22" height="91"/>
      <rect class="loader__leg" x="76" y="20" width="22" height="91"/>
      <rect class="loader__win" x="28" y="92" width="10" height="10"/>
      <rect class="loader__win" x="82" y="92" width="10" height="10"/>
      <g class="loader__bits"><rect x="23" y="116" width="3" height="6" style="--d:0s"/><rect x="29" y="116" width="3" height="9" style="--d:0.15s"/><rect x="35" y="116" width="3" height="5" style="--d:0.3s"/><rect x="41" y="116" width="3" height="7" style="--d:0.45s"/><rect x="77" y="116" width="3" height="7" style="--d:0.1s"/><rect x="83" y="116" width="3" height="5" style="--d:0.25s"/><rect x="89" y="116" width="3" height="9" style="--d:0.4s"/><rect x="95" y="116" width="3" height="6" style="--d:0.55s"/></g>
    </svg>
    <p class="loader__text"><span>Loading</span><span class="loader__pct" data-loader-pct>0%</span></p>
  </div>
  <a class="skip" href="#main">Skip to content</a>

  <header class="site-header" id="header">
    <div class="wrap site-header__inner">
      <a href="{home or '#top'}" class="brand">nidheesh narayanan</a>
      <nav class="site-nav" aria-label="Primary">{nav}
      </nav>
      <a href="mailto:{EMAIL}" class="button button--small site-header__cta">Get in touch {ARROW}</a>
      <button type="button" class="menu-toggle" aria-expanded="false" aria-controls="menu">Menu</button>
    </div>
  </header>

  <div class="menu" id="menu" hidden inert>
    <nav aria-label="Mobile">{mnav}
    </nav>
    <p class="menu__foot"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
  </div>
'''

def wordmark(tag='p', hidden=True):
    aria = ' aria-hidden="true"' if hidden else ''
    return f'<{tag} class="wordmark" data-fit{aria}><span class="wordmark__clip"><span class="wordmark__inner">nidheesh narayanan</span></span></{tag}>'

def footer(home, prefix):
    TURN = '<svg class="tile__icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M8.5 7H17v8.5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
    return f'''
  <footer class="footer wrap" id="contact">
    <div class="talk">
      <div class="talk__intro">
        <h2 class="talk__title">Have a project or a role in mind? <span>Let’s talk.</span></h2>
        <p class="talk__note">Open to full-time roles and freelance work.</p>
        <p class="talk__meta mono">Dubai <span data-clock>--:--</span>, GMT+4</p>
      </div>
      <ul class="tiles" role="list">
        <li class="tile tile--wide">
          <a class="tile__link" href="mailto:{EMAIL}"><span class="tile__label">Email</span><span class="tile__value">{EMAIL}</span>{TURN}</a>
          <button type="button" class="tile__copy" data-copy="{EMAIL}">Copy</button>
          <span class="sr-only" role="status" data-copy-status></span>
        </li>
        <li class="tile tile--wide">
          <a class="tile__link" href="{LINKEDIN}" target="_blank" rel="noopener noreferrer"><span class="tile__label">LinkedIn</span><span class="tile__value">View profile</span>{TURN}<span class="sr-only"> (opens in new tab)</span></a>
        </li>
      </ul>
    </div>
    <div class="footer__bar">
      <nav class="footer__nav" aria-label="Footer">
        <a href="{home}#work">Work</a>
        <a href="{home}#services">Services</a>
        <a href="{home}#about">About</a>
      </nav>
      <span class="mono">© <span data-year>2026</span> Nidheesh Narayanan</span>
      <a href="#top" class="footer__top">Back to top <svg viewBox="0 0 14 14" aria-hidden="true"><path d="M7 12V2.5M2.8 6.7 7 2.5l4.2 4.2" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></a>
    </div>
    {wordmark()}
  </footer>
'''

SCRIPTS = lambda prefix: f'''
  <script src="{prefix}assets/js/vendor/lenis.min.js" defer></script>
  <script src="{prefix}assets/js/main.js?v={ASSET_V}" defer></script>
</body>
</html>
'''

# ---------------- index ----------------
def tags(slug, sector, langs, plat):
    items = [plat.split(',')[0], 'Arabic RTL' if 'Arabic' in langs else None, sector]
    return ''.join(f'<li>{html.escape(t)}</li>' for t in items if t)

rows = []
for k, (slug, name, sector, langs, plat, host) in enumerate(P[:6]):
    rows.append(f'''        <li class="project">
          <a class="project__link" href="work/{slug}.html">
            <span class="project__media">
              <img class="project__shot" src="assets/img/works/{slug}.webp" width="1440" height="900" alt="" loading="lazy" decoding="async">
              <span class="project__phone"><img src="assets/img/works/{slug}-mobile-390.webp" width="390" height="844" alt="" loading="lazy" decoding="async"></span>
              <span class="project__view">View case study</span>
            </span>
            <div class="project__info">
              <span class="project__top"><span class="project__num mono">{k + 1:02d}</span>{badge(slug)}</span>
              <span class="project__name">{html.escape(name)}</span>
              <span class="project__desc">{html.escape(intro[slug])}</span>
              <ul class="tags" role="list">{tags(slug, sector, langs, plat)}</ul>
            </div>
          </a>
        </li>''')
more = []
for slug, name, sector, langs, plat, host in P[6:]:
    more.append(f'''          <li><a href="work/{slug}.html"><span class="more__name">{html.escape(name)}{badge(slug)}</span><span class="more__sector">{html.escape(sector)}</span><span class="more__go">Case study</span></a></li>''')

SERVICES = [
    ('WordPress builds', 'Custom themes and Elementor widgets for enterprise sites, with WPML or Polylang for English and Arabic.', 'assets/img/gallery/laptop-dubai.webp'),
    ('Frontend engineering', 'React, Next.js and TypeScript interfaces, reusable components, and motion with GSAP.', 'assets/img/gallery/code.webp'),
    ('Arabic and RTL', 'Right-to-left layouts that are designed for Arabic, not mirrored as an afterthought.', 'assets/img/gallery/calligraphy.webp'),
    ('Speed and accessibility', 'Core Web Vitals work, WCAG 2.1 AA for government portals, and multilingual SEO.', 'assets/img/gallery/light-trails.webp'),
    ('Hosting and care', 'Servers, DNS, SSL, migrations and staging. When something breaks, I fix the cause.', 'assets/img/gallery/mashrabiya.webp'),
]
from PIL import Image as _Im
def _wh(path):
    w, h = _Im.open(path).size
    return f'width="{w}" height="{h}"'
svc_imgs = '\n'.join(f'          <img src="{img}" {_wh(img)} alt="" loading="lazy" decoding="async"{" class=\"is-active\"" if i == 0 else ""}>' for i, (_, _, img) in enumerate(SERVICES))
svc_list = '\n'.join(f'''          <li class="service{" is-active" if i == 0 else ""}" data-service="{i}">
            <h3>{t}</h3>
            <p><span>{d}</span></p>
          </li>''' for i, (t, d, _) in enumerate(SERVICES))

FAQ = [
    ('Are you available for new work?', 'Yes. I’m open to full-time roles and to freelance projects. The quickest way to reach me is by email or on LinkedIn.'),
    ('Do you build sites in Arabic?', 'Yes. Six of the projects above run in English and Arabic. I set up WPML or Polylang, build the right-to-left layouts, and check typography, forms and menus in both languages.'),
    ('Can you take over an existing WordPress site?', 'Yes. I can audit it, fix what is broken, speed it up and keep it updated, whether it was built with a custom theme or with Elementor.'),
    ('Which tools do you use?', 'WordPress, Elementor, WPML, PHP, MySQL, React, Next.js, TypeScript, SCSS, GSAP, Webflow, Drupal, Git and Figma.'),
    ('Where are you based?', 'Dubai, UAE (GMT+4). I work on site with teams in Dubai and remotely with teams elsewhere.'),
]
faq = '\n'.join(f'''          <details class="qa">
            <summary>{q}</summary>
            <p class="qa__a">{a}</p>
          </details>''' for q, a in FAQ)

index = head('Nidheesh Narayanan | Senior Frontend Developer in Dubai: React, Next.js &amp; WordPress',
             'Senior frontend developer in Dubai working in React, Next.js and WordPress. Fast, accessible websites in English and Arabic for UAE government bodies and brands.', '',
             f'  <link rel="preload" as="image" href="assets/img/me/portrait-back.webp?v={ASSET_V}" imagesrcset="assets/img/me/portrait-back-760.webp?v={ASSET_V} 646w, assets/img/me/portrait-back.webp?v={ASSET_V} 1191w" imagesizes="(max-width: 760px) 90vw, 50vw" fetchpriority="high">\n') + \
'''  <script type="application/ld+json">{"@context": "https://schema.org", "@graph": [{"@type": "Person", "@id": "{{SITE_URL}}/#person", "name": "Nidheesh Narayanan", "url": "{{SITE_URL}}/", "image": "{{SITE_URL}}/assets/img/og.jpg", "jobTitle": "Senior Frontend Developer", "worksFor": {"@type": "Organization", "name": "GTECH Information Technology"}, "email": "mailto:hello.nidheesh@gmail.com", "address": {"@type": "PostalAddress", "addressLocality": "Dubai", "addressCountry": "AE"}, "sameAs": ["https://www.linkedin.com/in/nidheesh-narayanan-b9180853/"], "knowsLanguage": ["English", "Malayalam", "Hindi", "Tamil"], "knowsAbout": ["WordPress", "Elementor", "WPML", "PHP", "React", "Next.js", "TypeScript", "Web accessibility", "WCAG 2.1", "Arabic RTL websites", "Core Web Vitals", "Multilingual SEO"]}, {"@type": "WebSite", "@id": "{{SITE_URL}}/#website", "url": "{{SITE_URL}}/", "name": "Nidheesh Narayanan", "inLanguage": "en", "publisher": {"@id": "{{SITE_URL}}/#person"}}, {"@type": "ProfilePage", "@id": "{{SITE_URL}}/#profile", "url": "{{SITE_URL}}/", "name": "Nidheesh Narayanan | Senior Frontend Developer in Dubai: React, Next.js & WordPress", "mainEntity": {"@id": "{{SITE_URL}}/#person"}, "isPartOf": {"@id": "{{SITE_URL}}/#website"}}]}</script>
</head>
''' + header('', '') + f'''
  <main id="main">
    <!-- ========== HERO ========== -->
    <section class="hero" id="top" aria-labelledby="hero-title">
      <span class="hero__glow" aria-hidden="true"></span>
      <span class="hero__glow hero__glow--two" aria-hidden="true"></span>
      <span class="hero__light" aria-hidden="true"></span>
      <div class="hero__orbit" aria-hidden="true">
        <svg class="orbit orbit--text" viewBox="0 0 600 600"><defs><path id="orbit-path" d="M300,300 m-262,0 a262,262 0 1,1 524,0 a262,262 0 1,1 -524,0"/></defs><text><textPath href="#orbit-path" textLength="1640" lengthAdjust="spacing">WordPress / React &amp; Next.js / Arabic &amp; RTL / Accessibility / Performance / Dubai, UAE / WordPress / React &amp; Next.js / Arabic &amp; RTL / Accessibility / Performance / Dubai, UAE / </textPath></text></svg>
      </div>
      <img class="hero__photo" src="assets/img/me/portrait-back.webp?v={ASSET_V}" srcset="assets/img/me/portrait-back-760.webp?v={ASSET_V} 646w, assets/img/me/portrait-back.webp?v={ASSET_V} 1191w" sizes="(max-width: 760px) 90vw, 50vw" width="1191" height="1400" alt="Nidheesh Narayanan, seen from behind" fetchpriority="high" decoding="async">
      <div class="hero__intro">
        <h1 class="hero__title" id="hero-title" data-fit-lines><span class="hl">Websites for</span> <span class="hl">government</span> <span class="hl">and brands,</span> <span class="hl">in English</span> <span class="hl">and Arabic.</span></h1>
        <p class="hero__lede">I’m Nidheesh. For nine years I’ve built fast, accessible sites for UAE public bodies and companies.</p>
        <div class="hero__actions">
          <a href="#work" class="button">See the work</a>
        </div>
      </div>
      <div class="hero__foot wrap">
        <p class="hero__meta mono"><span>Frontend developer <span class="hero__stack">React / Next.js / WordPress</span></span><span>Dubai, UAE</span></p>
        {wordmark()}
      </div>
    </section>

    <!-- ========== STATEMENTS: scroll-linked, dark to light ========== -->
    <section class="statements" data-statements aria-label="What I do, in short">
      <div class="statements__sticky">
        <span class="statements__bg" aria-hidden="true"></span>
        <span class="statements__dots" aria-hidden="true"></span>
        <p class="statement split" data-split>Nine years of websites for Dubai’s government and its best-known brands.</p>
        <p class="statement split" data-split>In English and Arabic. Fast on any phone. Usable by everyone.</p>
        <p class="statement statement--ink split" data-split>For most people, your website is the first office they walk into.</p>
      </div>
    </section>

    <!-- ========== WORK ========== -->
    <section class="work wrap" id="work" aria-labelledby="work-title">
      <div class="section-head">
        <h2 id="work-title">Selected work</h2>
        <p>11 projects</p>
      </div>
      <!-- Each row opens a case-study page in /work/. Order and text come from the build script. -->
      <ol class="projects" role="list">
{chr(10).join(rows)}
      </ol>
      <div class="more">
        <h3>More projects</h3>
        <ol role="list">
{chr(10).join(more)}
        </ol>
      </div>
    </section>

    <!-- ========== SERVICES ========== -->
    <section class="section services dark wrap" id="services" aria-labelledby="services-title" data-theme="dark">
      <div class="section-head">
        <h2 id="services-title">What I do</h2>
      </div>
      <div class="services__grid">
        <div class="services__media" aria-hidden="true">
{svc_imgs}
        </div>
        <ul class="services__list" role="list">
{svc_list}
        </ul>
      </div>
      <div class="services__note split" data-split-scroll>
        <p>From design file to live server: theme, Arabic version, speed, hosting, and the fixes that come after launch.</p>
      </div>
    </section>

    <!-- ========== ABOUT ========== -->
    <section class="section wrap" id="about" aria-labelledby="about-title">
      <div class="section-head">
        <h2 id="about-title">About</h2>
      </div>
      <div class="about__grid">
        <p class="about__lead">Most of my work is for government bodies and large companies in the UAE, where sites have to load fast, meet accessibility rules and read as well in Arabic as in English.</p>
        <p>I work with designers, backend engineers and project managers in Agile teams, and I use AI coding tools to move faster without lowering the bar.</p>
        <div class="about__side">
          <div>
            <h3 class="mono">Experience</h3>
            <ol class="timeline" role="list">
              <li><span class="yrs">2021–now</span><span><strong>Senior Frontend Developer</strong>GTECH Information Technology, Dubai</span></li>
              <li><span class="yrs">2018–2021</span><span><strong>Frontend Developer</strong>Belong Digital, Dubai</span></li>
              <li><span class="yrs">2011–2017</span><span><strong>Frontend Developer and Web Designer</strong>Agencies and freelance, India</span></li>
            </ol>
          </div>
          <div>
            <h3 class="mono">Education</h3>
            <p>Diploma in Advanced VFX and Multimedia, Keltron<br>B.Com, Calicut University</p>
          </div>
          <div>
            <h3 class="mono">Languages</h3>
            <p>English, Malayalam, Hindi, Tamil</p>
          </div>
        </div>
        <div class="clients">
          <h3 class="mono">Clients</h3>
          <p>QuantumGate, Dubai Women Establishment, MBZUAI, Dubai International Boat Show, World Police Summit, Gulfood Manufacturing, Ducab, AI71, UAE Gender Balance Council, Future Health Initiative, PayFuture, Dhamani 1969, LODD, Gulf Beverages and HQWS.</p>
        </div>
      </div>
    </section>

    <!-- ========== FAQ + CTA ========== -->
    <section class="section dark wrap" aria-labelledby="faq-title" data-theme="dark">
      <div class="section-head">
        <h2>Questions</h2>
      </div>
      <div class="faq__grid">
        <h2 class="faq__title" id="faq-title">Things people usually ask first.</h2>
        <div class="faq__list">
{faq}
        </div>
      </div>
    </section>
  </main>
''' + footer('', '') + SCRIPTS('')
open('index.html', 'w').write(index)

# ---------------- case pages: keep their content, swap the shell ----------------
for slug, name, *_ in P:
    f = f'work/{slug}.html'
    s = open(f).read()
    main = s[s.index('<main id="main"'):s.index('</main>') + len('</main>')]
    main = main.replace('<main id="main" class="wrap">', '<main id="main" class="case wrap">')
    main = re.sub(r'\n\s*<!-- TODO \(Nidheesh\).*?-->', '', main)
    main = re.sub(r'\s*<span class="gov-badge[^"]*">.*?</span>(?=\s*<h1)', '', main)
    if slug in GOV:
        main = main.replace('      <h1 class="case-title">', '      ' + badge(slug, 'gov-badge gov-badge--case') + '\n      <h1 class="case-title">', 1)
    main = main.replace('class="scroller" tabindex="0"', 'class="scroller" data-lenis-prevent tabindex="0"')
    title = f'{html.escape(name)} website | Nidheesh Narayanan'
    d_full = f'{html.unescape(intro[slug])} Case study by Nidheesh Narayanan.'
    desc = html.escape(d_full if len(d_full) <= 160 else html.unescape(intro[slug]))
    host = dict((x[0], x[5]) for x in P)[slug]
    ld = ('  <script type="application/ld+json">{"@context": "https://schema.org", "@graph": ['
          '{"@type": "CreativeWork", "name": "' + name + ' website", "url": "{{SITE_URL}}/work/' + slug + '", "description": "' + html.unescape(intro[slug]).replace('"', '\\"') + '", '
          '"creator": {"@type": "Person", "@id": "{{SITE_URL}}/#person", "name": "Nidheesh Narayanan"}, "about": {"@type": "WebSite", "url": "https://' + host + '"}}, '
          '{"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "{{SITE_URL}}/"}, '
          '{"@type": "ListItem", "position": 2, "name": "Work", "item": "{{SITE_URL}}/#work"}, {"@type": "ListItem", "position": 3, "name": "' + name + '", "item": "{{SITE_URL}}/work/' + slug + '"}]}]}</script>\n')
    page = head(title, desc, '../', ld, f'og/{slug}.jpg', f'{html.escape(name)} website, built by Nidheesh Narayanan') + '</head>\n' + header('../index.html', '../') + '\n  ' + main + '\n' + footer('../index.html', '../') + SCRIPTS('../')
    open(f, 'w').write(page)
print('ok')

# ---------------- 404 (served by Cloudflare Pages for any missing URL, so it uses root-absolute paths) ----------------
nf = head('Page not found | Nidheesh Narayanan', 'This page does not exist. Go back to the portfolio of Nidheesh Narayanan, frontend and WordPress developer in Dubai.', '/').replace(
    '<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">') + '</head>\n' + header('/', '/') + '''
  <main id="main" class="case wrap">
    <header class="case-head">
      <a class="case-back" href="/">Home</a>
      <h1 class="case-title">This page doesn’t exist.</h1>
      <p class="case-intro">The link may be old or mistyped. The work, services and contact details are all on the home page.</p>
      <p class="hero__actions"><a href="/#work" class="button">See the work</a><a href="/#contact" class="hero__link">Get in touch</a></p>
    </header>
  </main>
''' + footer('/', '/') + SCRIPTS('/')
open('404.html', 'w').write(nf)
print('404 ok')
