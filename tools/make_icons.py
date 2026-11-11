"""Social image (1200x630), favicons and web manifest. Needs the TTFs in tools/fonts/ (Schibsted Grotesk variable, IBM Plex Mono Medium)."""
import os, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
os.chdir(ROOT)
F = 'tools/fonts/'
PAPER, INK, MUTED = (236, 236, 235), (23, 23, 23), (97, 97, 97)

def font(size, weight=700):
    f = ImageFont.truetype(F + 'schibsted.ttf', size)
    f.set_variation_by_axes([weight])
    return f

# ---------- social card ----------
W, H = 1200, 630
card = Image.new('RGB', (W, H), PAPER)
glow = Image.new('L', (W, H), 0)
ImageDraw.Draw(glow).ellipse((620, -160, 1260, 480), fill=255)
glow = glow.filter(ImageFilter.GaussianBlur(110))
card = Image.composite(Image.new('RGB', (W, H), (250, 250, 250)), card, glow)
me = Image.open('assets/img/me/portrait-back.webp').convert('RGBA')
mh = 600
me = me.resize((round(me.width * mh / me.height), mh), Image.LANCZOS)
# fade the bottom of the portrait into the paper
fade = Image.linear_gradient('L').resize(me.size).point(lambda v: 255 if v < 150 else max(0, 255 - (v - 150) * 2.4))
alpha = Image.composite(me.getchannel('A'), Image.new('L', me.size, 0), fade)
me.putalpha(alpha)
card.paste(me, (W - me.width + 40, H - mh), me)
d = ImageDraw.Draw(card)
d.line((60, 92, 92, 92), fill=MUTED, width=2)
d.text((106, 80), 'Senior frontend and WordPress developer, Dubai', font=font(24, 500), fill=MUTED)
y = 140
for line in ['Websites for', 'government and', 'brands, in English', 'and Arabic.']:
    d.text((56, y), line, font=font(64, 700), fill=INK)
    y += 66
d.text((58, 470), 'nidheesh narayanan', font=font(78, 800), fill=INK)
d.text((60, 572), 'WORDPRESS  /  REACT  /  ARABIC & RTL  /  ACCESSIBILITY', font=ImageFont.truetype(F + 'plexmono.ttf', 18), fill=MUTED)
card.save('assets/img/og.jpg', 'JPEG', quality=86, optimize=True, progressive=True)

# ---------- favicons ----------
svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#171717"/>'
       '<path d="M19 47V24h6.6v3.4c1.7-2.6 4.3-4 7.7-4 5.3 0 8.7 3.5 8.7 9.4V47h-6.8V34.2c0-3.4-1.6-5.2-4.6-5.2-3.2 0-5 2.1-5 5.8V47z" fill="#ececeb"/>'
       '<circle cx="47.5" cy="43.5" r="3.5" fill="#ececeb"/></svg>')
open('favicon.svg', 'w').write(svg)

def icon(size, pad=0.0, radius=0.22):
    S = size * 4
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle((0, 0, S - 1, S - 1), radius=int(S * radius), fill=INK)
    f = font(int(S * 0.72), 800)
    bb = dr.textbbox((0, 0), 'n', font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    x = (S - tw) / 2 - bb[0] - S * 0.05
    yy = (S - th) / 2 - bb[1]
    dr.text((x, yy), 'n', font=f, fill=PAPER)
    r = S * 0.055
    cx, cy = x + bb[2] + S * 0.07, yy + bb[3] - r
    dr.ellipse((cx - r, cy - r, cx + r, cy + r), fill=PAPER)
    return im.resize((size, size), Image.LANCZOS)

icon(32).save('favicon-32.png')
icon(180, radius=0).save('apple-touch-icon.png')
icon(192).save('assets/img/icon-192.png')
icon(512).save('assets/img/icon-512.png')
icon(48).save('favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
json.dump({
    'name': 'Nidheesh Narayanan', 'short_name': 'Nidheesh',
    'description': 'Senior frontend and WordPress developer in Dubai.',
    'start_url': '/', 'display': 'browser', 'background_color': '#ececeb', 'theme_color': '#ececeb',
    'icons': [{'src': '/assets/img/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
              {'src': '/assets/img/icon-512.png', 'sizes': '512x512', 'type': 'image/png'}],
}, open('site.webmanifest', 'w'), indent=2)
print('ok')
