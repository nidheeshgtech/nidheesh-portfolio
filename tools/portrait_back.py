"""Back-view portrait: Vision mask + duotone -> transparent WebP for the hero. Usage: python3 portrait_back.py src.png mask.png"""
import sys
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

src, maskp = sys.argv[1], sys.argv[2]
OUT = '/Applications/MAMP/htdocs/nidheesh-portfolio-2026/assets/img/me/'
INK = (23, 23, 23)
LIGHT = (238, 238, 237)

im = Image.open(src).convert('RGB')
mask = Image.open(maskp).convert('L').resize(im.size, Image.LANCZOS)
g = ImageOps.grayscale(im)
g = ImageOps.autocontrast(g, cutoff=0.5)
g = ImageEnhance.Contrast(g).enhance(1.08)
tone = ImageOps.colorize(g, black=INK, white=LIGHT, mid=(124, 124, 123))
blur = max(1.5, im.width / 700)
a = mask.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: 0 if v < 16 else min(255, int((v - 16) * 1.1)))
out = tone.convert('RGBA'); out.putalpha(a)
bb = a.getbbox()
out = out.crop((bb[0], 0, im.width, im.height))   # keep the top/bottom/right edges as framed
for h, suf in [(1400, ''), (760, '-760')]:
    r = out.resize((round(out.width * h / out.height), h), Image.LANCZOS)
    r.save(f'{OUT}portrait-back{suf}.webp', 'WEBP', quality=82, method=6)
    print(suf or 'full', r.size)
prev = Image.new('RGBA', out.size, (230, 232, 225, 255)); prev.alpha_composite(out)
prev.convert('RGB').resize((out.width * 500 // out.height, 500)).save('/private/tmp/claude-502/-Applications-MAMP-htdocs-nidheesh-portfolio-2026/5dc78856-303b-4cbc-a949-b4ba5c326e1c/scratchpad/photo/prevback.jpg')
