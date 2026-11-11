"""Social images (1200x630: one for the site, one per case study), favicons and web manifest.
Needs the TTFs in tools/fonts/ (Schibsted Grotesk variable, IBM Plex Mono Medium).
  python3 tools/make_icons.py"""
import os, json, re, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
os.chdir(ROOT)
F = 'tools/fonts/'
PAPER, INK, INK2, MUTED, LINE = (236, 236, 235), (23, 23, 23), (56, 56, 56), (97, 97, 97), (200, 200, 197)
W, H = 1200, 630


def font(size, weight=700):
    f = ImageFont.truetype(F + 'schibsted.ttf', size)
    f.set_variation_by_axes([weight])
    return f


def mono(size):
    return ImageFont.truetype(F + 'plexmono.ttf', size)


# ---------- the "N" mark: same geometry as the page loader (viewBox 0 0 120 132, box 22..98 x 20..111) ----------
def n_mark(height, fg=INK, bg=None, pad=0.0, radius=0.0):
    """Capital N drawn at 4x and scaled down. With bg it sits on a (rounded) square tile."""
    S = 4
    nw, nh = 76, 91                                   # N box in loader units
    if bg is None:
        size = (round(height * nw / nh), height)
        k = height / nh
        ox, oy = -22 * k, -20 * k
    else:
        size = (height, height)
        k = height * (1 - 2 * pad) / nh
        ox, oy = (height - nw * k) / 2 - 22 * k, (height - nh * k) / 2 - 20 * k
    im = Image.new('RGBA', (size[0] * S, size[1] * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if bg is not None:
        d.rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius=int(im.width * radius), fill=bg)
    P = lambda x, y: ((ox + x * k) * S, (oy + y * k) * S)
    # diagonal, clipped to the N box
    diag = Image.new('L', im.size, 0)
    ImageDraw.Draw(diag).line([P(26.9, 9.7), P(93.1, 121.3)], fill=255, width=round(19 * k * S))
    clip = Image.new('L', im.size, 0)
    ImageDraw.Draw(clip).rectangle([P(22, 20), P(98, 111)], fill=255)
    diag = Image.composite(diag, Image.new('L', im.size, 0), clip)
    im.paste(Image.new('RGBA', im.size, fg + (255,)), (0, 0), diag)
    d.rectangle([P(22, 20), P(44, 111)], fill=fg)
    d.rectangle([P(76, 20), P(98, 111)], fill=fg)
    return im.resize(size, Image.LANCZOS)


def card_base():
    card = Image.new('RGB', (W, H), PAPER)
    glow = Image.new('L', (W, H), 0)
    ImageDraw.Draw(glow).ellipse((620, -160, 1260, 480), fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(110))
    return Image.composite(Image.new('RGB', (W, H), (250, 250, 250)), card, glow)


def brand(card, x=60, y=56):
    """N mark + name, top left."""
    m = n_mark(34)
    card.paste(m, (x, y), m)
    ImageDraw.Draw(card).text((x + m.width + 16, y + 17), 'Nidheesh Narayanan', font=font(26, 700), fill=INK, anchor='lm')


def wrap(text, f, maxw, draw):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if draw.textlength(t, font=f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    return lines + [cur]


def save(card, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    card.save(path, 'JPEG', quality=86, optimize=True, progressive=True)


# ---------- main social card ----------
card = card_base()
me = Image.open('assets/img/me/portrait-back.webp').convert('RGBA')
mh = 600
me = me.resize((round(me.width * mh / me.height), mh), Image.LANCZOS)
fade = Image.linear_gradient('L').resize(me.size).point(lambda v: 255 if v < 150 else max(0, 255 - (v - 150) * 2.4))
me.putalpha(Image.composite(me.getchannel('A'), Image.new('L', me.size, 0), fade))
card.paste(me, (W - me.width + 40, H - mh), me)
brand(card)
d = ImageDraw.Draw(card)
y = 150
for i, line in enumerate(['Websites for', 'government and', 'brands, in English', 'and Arabic.']):
    d.text((56, y), line, font=font(70, 700), fill=INK if i < 3 else INK2)
    y += 72
d.text((60, 482), 'Senior frontend developer in Dubai', font=font(30, 600), fill=INK)
d.text((60, 534), 'React  /  Next.js  /  WordPress  /  Arabic & RTL', font=mono(20), fill=MUTED)
save(card, 'assets/img/og.jpg')

# ---------- one card per case study ----------
src = open('tools/pages.py').read()
P = eval(src[src.index('P = [') + 4: src.index(']\n', src.index('P = [')) + 1])
GOV = eval(re.search(r'GOV = (\{[^}]*\})', src).group(1))
for slug, name, sector, langs, stack, host in P:
    card = card_base()
    shot = Image.open(f'assets/img/works/{slug}.webp').convert('RGB')
    sw = 690
    shot = shot.resize((sw, round(shot.height * sw / shot.width)), Image.LANCZOS)
    # browser frame with a soft shadow, bleeding off the right edge
    bar = 30
    frame = Image.new('RGB', (sw, shot.height + bar), (250, 250, 249))
    frame.paste(shot, (0, bar))
    fd = ImageDraw.Draw(frame)
    for i in range(3):
        fd.ellipse((14 + i * 16, 10, 24 + i * 16, 20), fill=LINE)
    fx, fy = 548, 150
    sh = Image.new('L', (W, H), 0)
    ImageDraw.Draw(sh).rounded_rectangle((fx + 6, fy + 18, fx + sw + 40, fy + frame.height + 30), 14, fill=70)
    card = Image.composite(Image.new('RGB', (W, H), (150, 150, 148)), card, sh.filter(ImageFilter.GaussianBlur(26)))
    mask = Image.new('L', frame.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, sw + 40, frame.height - 1), 12, fill=255)
    card.paste(frame, (fx, fy), mask)
    brand(card)
    d = ImageDraw.Draw(card)
    y = 150
    if slug in GOV:
        f = font(19, 600)
        tw = d.textlength(GOV[slug], font=f)
        d.rounded_rectangle((60, y, 60 + tw + 50, y + 36), 18, fill=INK)
        d.polygon([(78, y + 10), (86, y + 7), (94, y + 10), (94, y + 19), (86, y + 28), (78, y + 19)], fill=PAPER)
        d.text((102, y + 18), GOV[slug], font=f, fill=PAPER, anchor='lm')
        y += 58
    size = 66
    while True:
        f = font(size, 700)
        lines = wrap(name, f, 450, d)
        if len(lines) <= 3 and all(d.textlength(l, font=f) <= 450 for l in lines):
            break
        size -= 2
    for l in lines:
        d.text((56, y), l, font=f, fill=INK)
        y += round(size * 1.04)
    d.text((60, y + 18), f'{sector}. {langs}.', font=font(26, 500), fill=INK2)
    d.text((60, 534), f'{host}  /  {stack}', font=mono(19), fill=MUTED)
    save(card, f'assets/img/og/{slug}.jpg')

# ---------- favicons: capital N on an ink tile ----------
svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#171717"/>'
       '<g transform="translate(4.6 2.4) scale(.45)" fill="#ececeb"><clipPath id="c"><rect x="22" y="20" width="76" height="91"/></clipPath>'
       '<path d="M26.9 9.7L93.1 121.3" stroke="#ececeb" stroke-width="19" clip-path="url(#c)"/>'
       '<rect x="22" y="20" width="22" height="91"/><rect x="76" y="20" width="22" height="91"/></g></svg>')
open('favicon.svg', 'w').write(svg)
icon = lambda size, radius=0.22: n_mark(size, fg=PAPER, bg=INK, pad=0.2, radius=radius)
icon(32).save('favicon-32.png')
icon(180, radius=0).save('apple-touch-icon.png')
icon(192).save('assets/img/icon-192.png')
icon(512).save('assets/img/icon-512.png')
icon(48).save('favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
json.dump({
    'name': 'Nidheesh Narayanan', 'short_name': 'Nidheesh',
    'description': 'Senior frontend developer in Dubai. React, Next.js and WordPress.',
    'start_url': '/', 'display': 'browser', 'background_color': '#ececeb', 'theme_color': '#ececeb',
    'icons': [{'src': '/assets/img/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
              {'src': '/assets/img/icon-512.png', 'sizes': '512x512', 'type': 'image/png'}],
}, open('site.webmanifest', 'w'), indent=2)
print('ok')
