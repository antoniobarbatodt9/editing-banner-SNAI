"""QA sul file MP4 compresso finale (e sul master lossless).

uso: python3 qa.py DIR_ORIGINALE DIR_MASTER DIR_DISTRIBUZIONE layout.json report.json
(DIR_* = sequenze PNG 001.png... decodificate con ffmpeg)
"""
import sys, json
import numpy as np
from PIL import Image
sys.path.insert(0, __import__('os').path.dirname(__file__))
import compose as C

o_dir, m_dir, d_dir, lay_path, rep_path = sys.argv[1:6]
L = lambda d, i: np.array(Image.open(f'{d}/{i:03d}.png').convert('RGB')).astype(float)
lay = json.load(open(lay_path))['layout_per_frame']
N = len([f for f in __import__("os").listdir(o_dir) if f.endswith(".png")])
rep = {}

# 1) fedelta' compressione: PSNR distribuzione vs master
ps = []
for i in range(1, N + 1):
    mse = ((L(m_dir, i) - L(d_dir, i)) ** 2).mean(); ps.append(99 if mse == 0 else 10 * np.log10(255 ** 2 / mse))
rep['psnr_dist_vs_master_db'] = {'min': round(min(ps), 2), 'mean': round(float(np.mean(ps)), 2),
                                 'frame_min': int(np.argmin(ps) + 1)}

# 2) sfondo/titolo/CTA/disclaimer invariati: pixel fuori dalle card nuove e dalle zone pulse
def untouched_mask(i):
    m = np.ones(L(o_dir, 1).shape[:2], bool)
    for card, spec in C.TL.get(i, {}).items():
        x0, y0, x1, y1 = spec['box']; m[max(0, y0 - 2):y1 + 3, max(0, x0 - 2):x1 + 3] = False
    if i in C.PULSE:
        x0, y0, x1, y1 = C.PULSE[i]; m[y0:y1 + 1, x0:x1 + 1] = False
    return m
dm, do = [], []
for i in range(1, N + 1):
    mk = untouched_mask(i)
    dm.append(np.abs(L(m_dir, i) - L(o_dir, i))[mk].max())          # master: deve essere 0
    do.append(np.abs(L(d_dir, i) - L(o_dir, i))[mk].mean())         # distribuzione: solo rumore di compressione
rep['fuori_card_master_vs_originale_max_diff'] = float(max(dm))
rep['fuori_card_distribuzione_vs_originale_mean_abs'] = round(float(np.mean(do)), 3)
cy0, cy1 = C.QA_CTA_ROWS
cta = (slice(cy0, cy1), slice(0, L(o_dir, 1).shape[1]))   # fascia CTA (include il suo pulse)
rep['cta_distribuzione_vs_originale_mean_abs'] = round(float(np.mean([np.abs(L(d_dir, i)[cta] - L(o_dir, i)[cta]).mean() for i in range(1, N + 1)])), 3)

# 3) misure d'inchiostro sui fotogrammi di riposo
THR = 0.3   # soglia di copertura per l'ingombro d'inchiostro (bordi AA inclusi da 30%)
def ink_h(img, box, kind):
    x0, y0, x1, y1 = [int(round(v)) for v in box]
    sub = img[max(0, y0):y1, max(0, x0):x1]
    fill = np.array(C.A.CARD_FILL)
    if kind == 'orange':
        v = (sub[..., 0] - fill[0]) / (C.A.ORANGE_AMOUNT[0] - fill[0]); v = np.where(sub[..., 2] < 90, v, 0)
    else:
        v = (sub.max(-1) - fill.max()) / (C.A.WHITE.max() - fill.max())
    rows = np.where((v > THR).sum(1) > 0)[0]; cols = np.where((v > THR).sum(0) > 0)[0]
    if len(rows) == 0: return None
    return {'h': int(rows[-1] - rows[0] + 1), 'w': int(cols[-1] - cols[0] + 1)}

def measure(d, i):
    img = L(d, i); out = {}
    for card, el in lay[str(i)].items():
        bx = el['box']
        lx, ly, lh, lw = el['logo']; fx, fy, fh = el['fino']; ax, ay, ah, aw = el['amount']
        pad = 3
        out[card] = {
            'card_px': [bx[2] - bx[0] + 1, bx[3] - bx[1] + 1],
            'logo': ink_h(img, (lx - pad, ly - pad, lx + lw + pad, ly + lh + pad), 'white'),
            'fino_a': ink_h(img, (fx - pad, fy - pad, fx + 45 * fh / 10 + pad, fy + fh + 1), 'white'),
            'importo': ink_h(img, (ax - pad, ay - 1, ax + aw + pad, ay + ah + pad), 'orange' if card == 'snai' else 'white'),
        }
    return out
rep['misure_riposo_distribuzione'] = {f: measure(d_dir, f) for f in C.QA_REST}
rep['misure_riposo_master'] = {f: measure(m_dir, f) for f in C.QA_REST}

# 4) assenza di pulse/rimbalzo: variazione frame-to-frame dell'interno card
def interior(i, card, d):
    x0, y0, x1, y1 = C.TL[i][card]['box']; return L(d, i)[y0 + 4:y1 - 3, x0 + 4:x1 - 3]
stab = {}
for card, rng in [(c, range(f0, f1 + 1)) for c, f0, f1 in C.QA_STAB]:
    dd = [np.abs(interior(i + 1, card, m_dir) - interior(i, card, m_dir)).max() for i in rng if (i + 1) in rng]
    stab[f'{card}_f{rng.start}-{rng.stop - 1}_master_max_diff'] = float(max(dd))
    dd = [np.abs(interior(i + 1, card, d_dir) - interior(i, card, d_dir)).mean() for i in rng if (i + 1) in rng]
    stab[f'{card}_f{rng.start}-{rng.stop - 1}_dist_mean_abs'] = round(float(max(dd)), 3)
# confronto: nell'originale lo stesso riquadro SNAI cambia durante il pulse
x0, y0, x1, y1 = C.PH3['snai']
q0, q1 = C.QA_PULSE_ORIG
stab[f'originale_snai_f{q0}-{q1}_mean_abs_max'] = round(float(max(np.abs(L(o_dir, i + 1)[y0:y1, x0:x1] - L(o_dir, i)[y0:y1, x0:x1]).mean() for i in range(q0, q1))), 3)
rep['stabilita'] = stab
json.dump(rep, open(rep_path, 'w'), indent=1)
print(json.dumps(rep, indent=1))
