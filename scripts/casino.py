"""Linea Bonus Casino': compositor per formato (FORMAT=320x480, ...). Config in scripts/formats_casino/c<FORMAT>.py.

Principio: lo sfondo e' un gradiente STATICO (verificato: i frame vuoti coincidono entro 3 livelli), quindi il
clean plate e' la mediana di frame reali vuoti -> nessun pixel inventato. Sopra il plate si ridisegnano gli
elementi (logo, FINO A, importo) dagli asset forniti, alle misure uniformi, con le stesse posizioni/curve
dell'originale. Restano pixel ORIGINALI: sigla d'apertura, conteggi (non vanno toccati), CTA (con il suo pulse),
disclaimer, frame di glitch, e i simboli dell'esplosione di chiusura (matte per differenza col frame di riposo).

uso: FORMAT=320x480 python3 casino.py DIR_ORIG DIR_OUT layout.json
"""
import os, sys, json, importlib
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import assets as A

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAS = os.path.join(ROOT, '01_originali_ufficiali', 'asset_video_CASINO')
FMT = os.environ.get('FORMAT', '320x480')
C = importlib.import_module('formats_casino.c' + FMT)
S = 8


def _load(name, color=None):
    im = np.array(Image.open(os.path.join(CAS, name)).convert('RGBA')).astype(float)
    a = im[..., 3] / 255
    rgb = im[..., :3] if color is None else np.broadcast_to(np.array(color, float), a.shape + (3,)).copy()
    ys, xs = np.where(a > 0.02); a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]; rgb = rgb[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    ys, xs = np.where(a > 0.5)
    return {'rgb': rgb, 'a': a, 'top': ys.min(), 'left': xs.min(), 'h': ys.max() - ys.min() + 1, 'w': xs.max() - xs.min() + 1}

LOGO = {'goldbet': _load('logo_goldbet.png', C.WHITE), 'netbet': _load('logo_netbet.png', C.WHITE), 'snai': _load('logo_snai.png')}
FINO = _load('text_fino_a.png', C.WHITE)
AMT = {'goldbet': _load('text_2000.png', C.WHITE), 'netbet': _load('text_2000.png', C.WHITE), 'snai': _load('text_5000.png', C.ORANGE)}

_cache = {}
def draw(canvas_pm, canvas_a, asset, key, x, y, h, reveal=1.0, opacity=1.0):
    """disegna l'asset (ingombro pieno alto h, angolo alto-sinistro dell'ingombro in x,y) su canvas a S x.
    reveal < 1: visibile solo la frazione sinistra dell'ingombro (scrittura progressiva originale)."""
    sc = h * S / asset['h']; ck = (key, round(h, 3))
    if ck not in _cache:
        a = asset['a']; _cache[ck] = A.resize_rgba(asset['rgb'], a, max(1, int(round(a.shape[0] * sc))), max(1, int(round(a.shape[1] * sc))))
    rgb, a = _cache[ck]
    if reveal < 1:
        a = a.copy(); a[:, int(round((asset['left'] + asset['w'] * reveal) * sc)):] = 0
    X = int(round(x * S - asset['left'] * sc)); Y = int(round(y * S - asset['top'] * sc))
    H, W = canvas_a.shape; hh, ww = a.shape
    sx0, sy0 = max(0, -X), max(0, -Y); dx0, dy0 = max(0, X), max(0, Y); dx1, dy1 = min(W, X + ww), min(H, Y + hh)
    if dx1 <= dx0 or dy1 <= dy0: return
    aa = a[sy0:sy0 + dy1 - dy0, sx0:sx0 + dx1 - dx0][..., None] * opacity
    canvas_pm[dy0:dy1, dx0:dx1] = rgb[sy0:sy0 + dy1 - dy0, sx0:sx0 + dx1 - dx0] * aa + canvas_pm[dy0:dy1, dx0:dx1] * (1 - aa)
    canvas_a[dy0:dy1, dx0:dx1] = aa[..., 0] + canvas_a[dy0:dy1, dx0:dx1] * (1 - aa[..., 0])


def amt_w(op, h): return AMT[op]['w'] * h / AMT[op]['h']
def logo_w(op, h): return LOGO[op]['w'] * h / LOGO[op]['h']


def block_geom(op, cx, cy, s):
    """geometria di un blocco centrato (cx, cy) a scala s (1 = misure finali uniformi)."""
    hl, hf, ha, g1, g2 = C.H_LOGO * s, C.H_FINO * s, C.H_AMT * s, C.G1 * s, C.G2 * s
    left = cx - amt_w(op, ha) / 2
    top = cy - (hl + g1 + hf + g2 + ha) / 2
    return {'logo': (left + C.LOGO_DX.get(op, 0) * s, top, hl), 'fino': (left + 2 * s, top + hl + g1, hf),
            'amt': (left, top + hl + g1 + hf + g2, ha)}


def lerp_geom(g0, g1, t):
    return {k: tuple(a + (b - a) * t for a, b in zip(g0[k], g1[k])) for k in g0}


def render(frame_shape, items):
    """items: lista di (op, geom, reveal_logo, reveal_fino, amt_override) -> (pm, alpha) a risoluzione frame."""
    H, W = frame_shape
    pm = np.zeros((H * S, W * S, 3)); al = np.zeros((H * S, W * S))
    for op, g, rl, rf, amt_geom in items:
        x, y, h = g['logo']; draw(pm, al, LOGO[op], ('l', op), x, y, h, rl)
        x, y, h = g['fino']; draw(pm, al, FINO, ('f',), x, y, h, rf)
        x, y, h = amt_geom if amt_geom else g['amt']; draw(pm, al, AMT[op], ('a', op), x, y, h)
    pm = pm.reshape(H, S, W, S, 3).mean((1, 3)); al = al.reshape(H, S, W, S).mean((1, 3))
    return pm, al


def main(src, out, lay_path):
    os.makedirs(out, exist_ok=True)
    load = lambda i: np.array(Image.open(os.path.join(src, f'{i:03d}.png')).convert('RGB')).astype(float)
    n = len([f for f in os.listdir(src) if f.endswith('.png')])
    plate = np.median(np.stack([load(i) for i in C.PLATE_FRAMES]), 0)
    H, W = plate.shape[:2]
    y_keep = C.KEEP_ROWS_FROM                      # da qui in giu': CTA + disclaimer sempre originali
    rest = {op: block_geom(op, *C.FINAL_CENTER[op], 1.0) for op in C.FINAL_CENTER}
    ph2 = C.PHASE2_GEOM                           # geometria fase 2 (misure originali, logo GoldBet uniformato)
    layout = {}
    rest_render = None
    for i in range(1, n + 1):
        orig = load(i); o = orig.copy(); items = None; copy_rows = None
        fixes = [fx for fx in C.LOGO_FIX if i in fx['frames']]
        if fixes:                                   # fasi 1-2: solo i loghi riportati a misura/proporzioni ufficiali
            pmL = np.zeros((H * S, W * S, 3)); aL = np.zeros((H * S, W * S))
            for fx in fixes:
                x0, y0, x1, y1 = fx['old']
                o[y0 - 1:y1 + 2, x0 - 1:x1 + 2] = plate[y0 - 1:y1 + 2, x0 - 1:x1 + 2]
                x, y, h = fx['new']; draw(pmL, aL, LOGO[fx['op']], ('l', fx['op']), x, y, h)
            pm = pmL.reshape(H, S, W, S, 3).mean((1, 3)); al = aL.reshape(H, S, W, S).mean((1, 3))
            o = o * (1 - al[..., None]) + pm
            layout[i] = {fx['op'] + '_logo': fx['new'] for fx in fixes}
        elif i in C.REARRANGE:                      # riordino della pila con la curva originale
            t = C.REARRANGE[i]
            items = [(op, lerp_geom(ph2[op], rest[op], t), 1, 1, None) for op in ('goldbet', 'netbet')]
            if i in C.SNAI_COUNT_FRAMES: copy_rows = C.SNAI_COUNT_ROWS
        elif i in C.SNAI_COUNT_FRAMES:              # conteggio SNAI: pixel originali
            items = [(op, rest[op], 1, 1, None) for op in ('goldbet', 'netbet')]; copy_rows = C.SNAI_COUNT_ROWS
        elif i in C.SNAI_REVEAL:                    # comparsa logo/FINO A + importo che si assesta
            rl, rf, ta = C.SNAI_REVEAL[i]
            g = rest['snai']; x, y, h = g['amt']; w = amt_w('snai', h)
            cx0, cy0, s0 = C.SNAI_COUNT_AMT                       # importo del conteggio al f129 (centro, scala)
            cx1, cy1 = x + w / 2, y + h / 2
            s = s0 + (1 - s0) * ta; cx = cx0 + (cx1 - cx0) * ta; cy = cy0 + (cy1 - cy0) * ta
            amt = (cx - w * s / 2, cy - h * s / 2, h * s)
            items = [(op, rest[op], 1, 1, None) for op in ('goldbet', 'netbet')] + [('snai', g, rl, rf, amt)]
        elif i in C.GLITCH_NO_SNAI:
            items = [(op, rest[op], 1, 1, None) for op in ('goldbet', 'netbet')]
        elif C.REST[0] <= i <= C.REST[1]:           # riposo (pulse SNAI rimosso)
            items = [(op, rest[op], 1, 1, None) for op in ('goldbet', 'netbet', 'snai')]
        elif i in C.OUTRO:                          # esplosione di chiusura: simboli originali sopra
            if rest_render is None:
                pm, al = render((H, W), [(op, rest[op], 1, 1, None) for op in ('goldbet', 'netbet', 'snai')])
                rest_render = plate * (1 - al[..., None]) + pm
            ref = load(C.REST[1])
            d = np.abs(orig - ref).max(-1)
            import cv2
            m = cv2.dilate((d > C.OUTRO_THR).astype(np.uint8), np.ones((3, 3), np.uint8)).astype(np.float32)
            m = cv2.GaussianBlur(m, (0, 0), 0.7)[..., None]
            o[:y_keep] = (rest_render * (1 - m) + orig * m)[:y_keep]
            layout[i] = 'outro_matte'
        if items is not None:
            pm, al = render((H, W), items)
            comp = plate * (1 - al[..., None]) + pm
            if copy_rows:
                r0, r1 = copy_rows; comp[r0:r1 + 1] = orig[r0:r1 + 1]
            o[:y_keep] = comp[:y_keep]
            layout[i] = {op: {k: [round(v, 2) for v in vals] for k, vals in (amt and {**g, 'amt': amt} or g).items()}
                         for op, g, rl, rf, amt in items}
        Image.fromarray(np.clip(np.round(o), 0, 255).astype(np.uint8)).save(os.path.join(out, f'{i:03d}.png'))
    json.dump({'layout_per_frame': {str(k): v for k, v in layout.items()}}, open(lay_path, 'w'), indent=1, default=float)
    print('ok')


if __name__ == '__main__':
    main(*sys.argv[1:4])
