"""Tavole QA (originale sopra / MP4 distribuzione decodificato sotto). uso: qa_sheets.py DIR_ORIG DIR_DIST OUT_DIR"""
import sys
from PIL import Image, ImageDraw, ImageFont
O, D, OUT = sys.argv[1:4]
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13)
def sheet(frames, name, title, crop=(0, 0, 300, 600), z=1.0):
    cw, ch = crop[2] - crop[0], crop[3] - crop[1]; w, h = int(cw * z), int(ch * z)
    s = Image.new('RGB', (len(frames) * (w + 8) + 8, 2 * h + 90), (32, 32, 36)); d = ImageDraw.Draw(s)
    d.text((8, 6), title, font=F, fill=(255, 255, 255))
    d.text((8, 26), 'sopra: master originale 2.000€   |   sotto: corretto (MP4 distribuzione decodificato)', font=F, fill=(200, 200, 200))
    for k, i in enumerate(frames):
        x = 8 + k * (w + 8)
        s.paste(Image.open(f'{O}/{i:03d}.png').crop(crop).resize((w, h), Image.LANCZOS), (x, 48))
        s.paste(Image.open(f'{D}/{i:03d}.png').crop(crop).resize((w, h), Image.LANCZOS), (x, 68 + h))
        d.text((x + 2, 50 + h), f'f{i}  t={(i - 1) / 15:.2f}s', font=F, fill=(255, 210, 0))
    s.save(f'{OUT}/{name}.png')
sheet([47, 60, 100], '01_riposo_per_fase', 'Fotogrammi di riposo: WH solo (f47), bet365+WH (f60), tre card (f100)')
sheet([80, 82, 83, 84, 86, 87, 89, 91, 93], '02_ex_pulse_SNAI_f80-93', 'Prima / durante / dopo il vecchio pulse SNAI (f82-92)', (20, 160, 280, 400))
sheet([43, 44, 46, 52, 53, 54, 66, 67, 68, 76], '03_ingressi_senza_contatori', 'Ingressi: importi subito al valore finale (niente conteggio / niente 900->500)', (40, 100, 260, 500), 0.8)
sheet([62, 63, 64, 65, 66, 67, 70], '04_transizione_fase2_fase3', 'Transizione verso le tre card: le card nuove coprono sempre le originali', (40, 60, 260, 520), 0.8)
sheet([122, 123, 124, 125, 126, 127], '05_uscita', "Uscita: stessa curva di dissolvenza misurata sull'originale (a=0.95/0.52/0.26)", (40, 60, 260, 520), 0.8)
