"""Tavole QA (originale sopra / MP4 distribuzione decodificato sotto). uso: qa_sheets.py DIR_ORIG DIR_DIST OUT_DIR"""
import sys
from PIL import Image, ImageDraw, ImageFont
O, D, OUT = sys.argv[1:4]
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13)
def sheet(frames, name, title, crop=(0, 0, 300, 600), z=1.0):
    cw, ch = crop[2] - crop[0], crop[3] - crop[1]; w, h = int(cw * z), int(ch * z)
    s = Image.new('RGB', (len(frames) * (w + 8) + 8, 2 * h + 90), (32, 32, 36)); d = ImageDraw.Draw(s)
    d.text((8, 6), title, font=F, fill=(255, 255, 255))
    d.text((8, 26), 'sopra: master originale   |   sotto: corretto (MP4 distribuzione decodificato)', font=F, fill=(200, 200, 200))
    for k, i in enumerate(frames):
        x = 8 + k * (w + 8)
        s.paste(Image.open(f'{O}/{i:03d}.png').crop(crop).resize((w, h), Image.LANCZOS), (x, 48))
        s.paste(Image.open(f'{D}/{i:03d}.png').crop(crop).resize((w, h), Image.LANCZOS), (x, 68 + h))
        d.text((x + 2, 50 + h), f'f{i}  t={(i - 1) / 15:.2f}s', font=F, fill=(255, 210, 0))
    s.save(f'{OUT}/{name}.png')
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compose as C
for frames, name, title, crop, z in C.QA_SHEETS:
    sheet(list(frames), name, title, crop, z)
