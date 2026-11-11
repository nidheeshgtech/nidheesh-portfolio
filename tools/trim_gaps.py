"""Remove tall empty bands (sticky/pinned scroll sections that render blank in a full-page capture).
Usage: python3 tools/trim_gaps.py in.png out.png [max_gap_px=260]"""
import sys
from PIL import Image, ImageStat

src, dst = sys.argv[1], sys.argv[2]
MAX_GAP = int(sys.argv[3]) if len(sys.argv) > 3 else 260
im = Image.open(src).convert('RGB')
g = im.convert('L').resize((im.width // 4, im.height))
flat = []
for y in range(im.height):
    row = g.crop((0, y, g.width, y + 1))
    flat.append(ImageStat.Stat(row).stddev[0] < 2.2)   # a row with almost no detail
keep, y = [], 0
while y < im.height:
    if flat[y]:
        e = y
        while e < im.height and flat[e]:
            e += 1
        if e - y > MAX_GAP:                              # long empty band: keep only part of it
            keep.append((y, y + 120)); y = e; continue
        keep.append((y, e)); y = e
    else:
        e = y
        while e < im.height and not flat[e]:
            e += 1
        keep.append((y, e)); y = e
h = sum(b - a for a, b in keep)
out = Image.new('RGB', (im.width, h))
yy = 0
for a, b in keep:
    out.paste(im.crop((0, a, im.width, b)), (0, yy)); yy += b - a
out.save(dst)
print(f'{src.split("/")[-1]}: {im.height} -> {h}px')
