"""Tavola del conteggio ripristinato: originale sopra / MP4 corretto sotto. uso: FORMAT=.. qa_count.py DIR_ORIG DIR_DIST layout.json OUT.png"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compose as C
from PIL import Image, ImageDraw, ImageFont
O, D, LAY, OUT = sys.argv[1:5]
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 12)
lay = json.load(open(LAY))['layout_per_frame']
byc = {}
for f in sorted(C.COUNT):
    for c in C.COUNT[f]: byc.setdefault(c, []).append(f)
cw = 150
maxn = max(len(v) + 1 for v in byc.values())
s = Image.new('RGB', (maxn * (cw + 4) + 90, len(byc) * 150 + 10), (32, 32, 36)); d = ImageDraw.Draw(s)
for r, (c, fr) in enumerate(byc.items()):
    fr = fr + [fr[-1] + 1]
    for k, f in enumerate(fr):
        x, y, h, w = lay[str(f)][c]['amount']
        bx = C.TL[f][c]['box']
        crop = (max(0, bx[0]), max(0, int(y - h * 0.6)), min(bx[2], 10000), int(y + h) + 4)
        for j, src in enumerate([O, D]):
            im = Image.open(f'{src}/{f:03d}.png').crop(crop)
            im = im.resize((cw, int(im.height * cw / im.width)), Image.LANCZOS).crop((0, 0, cw, 66))
            s.paste(im, (88 + k * (cw + 4), 16 + r * 150 + j * 68))
        d.text((88 + k * (cw + 4), 2 + r * 150), f'f{f}' + (' finale' if k == len(fr) - 1 else ''), font=F, fill=(255, 210, 0))
    d.text((4, 36 + r * 150), c + '\norig', font=F, fill=(255, 255, 255)); d.text((4, 104 + r * 150), 'corretto', font=F, fill=(120, 255, 120))
s.save(OUT)
