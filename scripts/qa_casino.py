"""QA Bonus Casino'. uso: FORMAT=.. qa_casino.py DIR_ORIG DIR_MASTER DIR_DIST OUT_DIR"""
import os, sys, json, importlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
C = importlib.import_module('formats_casino.c' + os.environ.get('FORMAT', '320x480'))
O, M, D, OUT = sys.argv[1:5]
os.makedirs(OUT, exist_ok=True)
L = lambda d, i: np.array(Image.open(f'{d}/{i:03d}.png').convert('RGB')).astype(int)
N = len([f for f in os.listdir(O) if f.endswith('.png')])
rep = {}

def runs(img, y0, y1):
    a = img[y0:y1]; r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = ((a.min(2) > 150) & (a.max(2) - a.min(2) < 50)) | ((r > 170) & (r - b > 100) & (g < 170))
    rows = np.where(m.sum(1) > 0)[0]; out = []
    if not len(rows): return out
    s = p = rows[0]
    for rr in list(rows[1:]) + [10 ** 6]:
        if rr > p + 1:
            c = np.where(m[s:p + 1].sum(0) > 0)[0]; out.append({'y': [int(s + y0), int(p + y0)], 'h': int(p - s + 1), 'x': [int(c.min()), int(c.max())], 'w': int(c.max() - c.min() + 1)}); s = rr
        p = rr
    return out

for name, d in (('originale', O), ('master', M), ('distribuzione', D)):
    rep[f'misure_riposo_{name}'] = {f'f{f}': runs(L(d, f), 0, C.KEEP_ROWS_FROM) for f in C.QA_REST}

# stabilita' nella finestra di riposo (pulse SNAI eliminato), solo sopra la CTA
r0, r1 = C.REST
rep['riposo_master_max_diff_tra_frame'] = int(max(np.abs(L(M, i + 1)[:C.KEEP_ROWS_FROM] - L(M, i)[:C.KEEP_ROWS_FROM]).max() for i in range(r0, r1)))
rep['riposo_originale_max_diff_tra_frame'] = int(max(np.abs(L(O, i + 1)[:C.KEEP_ROWS_FROM] - L(O, i)[:C.KEEP_ROWS_FROM]).max() for i in range(r0, r1)))
# pixel invariati: CTA/disclaimer sempre; frame non toccati interamente
touched = set(int(k) for k in json.load(open(os.environ['LAYOUT']))['layout_per_frame'])
rep['cta_disclaimer_master_vs_originale_max_diff'] = int(max(np.abs(L(M, i)[C.KEEP_ROWS_FROM:] - L(O, i)[C.KEEP_ROWS_FROM:]).max() for i in range(1, N + 1)))
rep['frame_non_toccati_master_vs_originale_max_diff'] = int(max(np.abs(L(M, i) - L(O, i)).max() for i in range(1, N + 1) if i not in touched))
rep['frame_toccati'] = sorted(touched)
ps = []
for i in range(1, N + 1):
    mse = ((L(M, i) - L(D, i)) ** 2).mean(); ps.append(99 if mse == 0 else 10 * np.log10(255 ** 2 / mse))
rep['psnr_dist_vs_master_db'] = {'min': round(min(ps), 2), 'mean': round(float(np.mean(ps)), 2)}
json.dump(rep, open(f'{OUT}/qa_report.json', 'w'), indent=1)

F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13)
H0, W0 = L(O, 1).shape[:2]
def sheet(frames, name, title, crop=None, z=1.0, bright=False):
    crop = crop or (0, 0, W0, H0); w, h = int((crop[2] - crop[0]) * z), int((crop[3] - crop[1]) * z)
    s = Image.new('RGB', (len(frames) * (w + 6) + 6, 2 * h + 90), (32, 32, 36)); d = ImageDraw.Draw(s)
    d.text((8, 6), title, font=F, fill=(255, 255, 255)); d.text((8, 26), 'sopra: master originale   |   sotto: corretto (MP4 distribuzione decodificato)', font=F, fill=(200, 200, 200))
    f = (lambda im: im.point(lambda v: min(255, max(0, (v - 30) * 3)))) if bright else (lambda im: im)
    for k, i in enumerate(frames):
        x = 6 + k * (w + 6)
        s.paste(f(Image.open(f'{O}/{i:03d}.png').crop(crop).resize((w, h), Image.LANCZOS)), (x, 48))
        s.paste(f(Image.open(f'{D}/{i:03d}.png').crop(crop).resize((w, h), Image.LANCZOS)), (x, 68 + h))
        d.text((x + 2, 50 + h), f'f{i}  t={(i - 1) / 15:.2f}s', font=F, fill=(255, 210, 0))
    s.save(f'{OUT}/{name}.png')
for args in C.QA_SHEETS: sheet(*args)
print(json.dumps({k: v for k, v in rep.items() if not k.startswith('misure')}, indent=1))
