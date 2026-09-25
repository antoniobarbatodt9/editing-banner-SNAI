"""Ricostruisce la timeline corretta dei formati SNAI Bonus Sport (FORMAT=300x600 | 160x600).
   Timeline e misure di ogni formato: scripts/formats/f<FORMAT>.py

Principio: lo sfondo originale non viene mai inventato ne' ricostruito.
 - Ogni card nuova copre sempre per intero la card originale dello stesso frame
   (box nuovo >= box originale + 1 px), quindi nessun pixel di sfondo nascosto
   viene scoperto.
 - Fuori dalle card nuove i pixel restano quelli originali del frame.
 - Unica eccezione, necessaria per togliere il pulse SNAI (f82-85, f89-92): l'anello
   che la card ingrandita copriva viene riempito con i pixel ORIGINALI degli stessi
   punti nei frame 81 e 93 (sfondo scuro statico, in lenta dissolvenza), interpolati.
 - Uscita (f124-126): nel master le card sfumano verso il nero con opacita' misurata;
   la card nuova (che copre la vecchia) sfuma con la stessa curva.
"""
import os, sys, json
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import assets as A

S = 8                     # supersampling
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- configurazione del formato
import importlib
FMT = os.environ.get('FORMAT', '300x600')
_cfg = importlib.import_module('formats.f' + FMT)
globals().update({k: v for k, v in vars(_cfg).items() if not k.startswith('_') and k not in ('A',)})
RADIUS = getattr(_cfg, 'RADIUS', 11.0)
CARD_BORDER = np.array(getattr(_cfg, 'CARD_BORDER', A.CARD_BORDER))
NUDGE = getattr(_cfg, 'NUDGE', {})
EXIT_ALPHA = getattr(_cfg, 'EXIT_ALPHA', {})

def _asset(rgb, a):
    """le misure si riferiscono all'ingombro pieno (alpha > 50%): l'alone semitrasparente
    del file ufficiale (es. SNAI) e i bordi AA non contano nell'altezza."""
    ys, xs = np.where(a > 0.5)
    return {'rgb': rgb, 'a': a, 'top': ys.min(), 'left': xs.min(), 'h': ys.max() - ys.min() + 1, 'w': xs.max() - xs.min() + 1}
_logo = {n: _asset(*A.load_logo(n)) for n in ['bet365', 'snai', 'wh']}
_fino = _asset(*A.load_fino_a())
_amt = {n: _asset(*A.render_amount(t, c)) for n, (t, c) in CONTENT.items()}


def rrect_sdf(W, H, l, t, r, b, rad):
    """distanza (px, positiva all'interno) dal bordo di un rettangolo arrotondato, su griglia S."""
    ys = (np.arange(H) + 0.5) / S; xs = (np.arange(W) + 0.5) / S
    X, Y = np.meshgrid(xs, ys)
    cx, cy = (l + r) / 2, (t + b) / 2; hw, hh = (r - l) / 2 - rad, (b - t) / 2 - rad
    qx = np.abs(X - cx) - hw; qy = np.abs(Y - cy) - hh
    out = np.hypot(np.maximum(qx, 0), np.maximum(qy, 0)) + np.minimum(np.maximum(qx, qy), 0) - rad
    return -out


def card_layer(box, k, ca, region):
    """Rende card + contenuti a S x; restituisce (premult RGB, alpha) alla risoluzione del frame sulla region."""
    rx0, ry0, rx1, ry1 = region
    W, H = (rx1 - rx0 + 1) * S, (ry1 - ry0 + 1) * S
    x0, y0, x1, y1 = box
    l, t, r, b = x0 + 0.4 - rx0, y0 + 0.4 - ry0, x1 + 0.6 - rx0, y1 + 0.6 - ry0
    d = rrect_sdf(W, H, l, t, r, b, RADIUS)
    cov = np.clip(d * S + 0.5, 0, 1)                      # copertura (AA gestito dal downsample)
    g = np.where(d <= 1.2, 1.0, np.exp(-(d - 1.2) / 0.9))
    col = A.CARD_FILL + (CARD_BORDER - A.CARD_FILL) * g[..., None]
    pm = col * cov[..., None]; al = cov.copy()
    return pm, al, (l, t, r, b)


def paste(pm, al, rgb, a, x, y, opacity):
    """compone (over) una maschera rgb/a gia' in scala S alla posizione float (x,y) in px-S."""
    xi, yi = int(round(x)), int(round(y)); h, w = a.shape
    H, W = al.shape
    sx0, sy0 = max(0, -xi), max(0, -yi); dx0, dy0 = max(0, xi), max(0, yi)
    dx1, dy1 = min(W, xi + w), min(H, yi + h)
    if dx1 <= dx0 or dy1 <= dy0: return
    aa = a[sy0:sy0 + dy1 - dy0, sx0:sx0 + dx1 - dx0] * opacity
    cc = rgb[sy0:sy0 + dy1 - dy0, sx0:sx0 + dx1 - dx0]
    pm[dy0:dy1, dx0:dx1] = cc * aa[..., None] + pm[dy0:dy1, dx0:dx1] * (1 - aa[..., None])
    al[dy0:dy1, dx0:dx1] = aa + al[dy0:dy1, dx0:dx1] * (1 - aa)


_cache = {}
def place(pm, al, key, asset, x, y, h, ox, oy, opacity):
    """disegna l'asset con ingombro pieno alto h px e angolo alto-sinistro dell'ingombro in (x, y)."""
    sc = h * S / asset['h']
    ck = (key, round(h, 3))
    if ck not in _cache:
        a = asset['a']
        _cache[ck] = A.resize_rgba(asset['rgb'], a, max(1, int(round(a.shape[0] * sc))), max(1, int(round(a.shape[1] * sc))))
    rgb, a = _cache[ck]
    paste(pm, al, rgb, a, (x - ox) * S - asset['left'] * sc, (y - oy) * S - asset['top'] * sc, opacity)


def layout(card, box, k):
    """posizioni (px frame, float) degli elementi: restituisce dict con x,y,h per logo/fino/amount."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1 + 1) / 2, (y0 + y1 + 1) / 2
    hl, hf, ha, g1, g2 = H_LOGO * k, H_FINO * k, H_AMT * k, G1 * k, G2 * k
    if abs(k - K2) < 1e-6:                                # fasi 1-2 a riposo: misure intere
        hl, hf, ha = round(hl), round(hf), round(ha)
    top = cy - (hl + g1 + hf + g2 + ha) / 2
    lw = _logo[card]['w'] * hl / _logo[card]['h']
    aw = _amt[card]['w'] * ha / _amt[card]['h']
    amt_x = cx - aw / 2
    # righe allineate alla griglia dei pixel: altezze d'inchiostro nitide e identiche tra le card
    y_logo = round(top); y_fino = round(top + hl + g1); y_amt = round(top + hl + g1 + hf + g2)
    dl, da = NUDGE.get(card, (0, 0))                      # ritocchi richiesti (px a scala 1)
    y_logo += round(dl * k); y_fino += round(da * k); y_amt += round(da * k)
    return {'logo': (cx - lw / 2, y_logo, hl, lw), 'fino': (amt_x + 2 * k, y_fino, hf),
            'amount': (amt_x, y_amt, ha, aw)}


def render_card(card, spec):
    box, k, ca = spec['box'], spec['k'], spec['ca']
    region = (box[0] - 2, box[1] - 2, box[2] + 2, box[3] + 2)
    pm, al, _ = card_layer(box, k, ca, region)
    L = layout(card, box, k)
    ox, oy = region[0], region[1]
    x, y, h, _ = L['logo']; place(pm, al, ('logo', card), _logo[card], x, y, h, ox, oy, ca)
    x, y, h = L['fino']; place(pm, al, ('fino',), _fino, x, y, h, ox, oy, ca)
    x, y, h, _ = L['amount']; place(pm, al, ('amt', card), _amt[card], x, y, h, ox, oy, ca)
    Hh, Ww = al.shape
    pm_d = pm.reshape(Hh // S, S, Ww // S, S, 3).mean((1, 3))
    al_d = al.reshape(Hh // S, S, Ww // S, S).mean((1, 3))
    return region, pm_d, al_d, L


def main(src_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    load = lambda i: np.array(Image.open(os.path.join(src_dir, f'{i:03d}.png')).convert('RGB')).astype(float)
    n = len([f for f in os.listdir(src_dir) if f.endswith('.png')])
    p0, p1 = PULSE_SRC; f81, f93 = load(p0), load(p1)
    report = {}
    for i in range(1, n + 1):
        orig = load(i); out = orig.copy()
        if i in PULSE:
            x0, y0, x1, y1 = PULSE[i]; w = (i - p0) / (p1 - p0)
            out[y0:y1 + 1, x0:x1 + 1] = (1 - w) * f81[y0:y1 + 1, x0:x1 + 1] + w * f93[y0:y1 + 1, x0:x1 + 1]
        a = EXIT_ALPHA.get(i, 1.0)
        rep = {}
        for card, spec in TL.get(i, {}).items():
            region, pm, al, L = render_card(card, spec)
            rx0, ry0, rx1, ry1 = region
            sl = (slice(ry0, ry1 + 1), slice(rx0, rx1 + 1))
            if a >= 1.0:
                out[sl] = out[sl] * (1 - al[..., None]) + pm
            else:
                # uscita: nel master le card sfumano verso il nero (misurato: sotto la card il fondo
                # e' nero ~(16,15,16.5), non la texture). La card nuova sfuma allo stesso modo.
                D = np.array([16., 15., 16.5])
                out[sl] = out[sl] * (1 - al[..., None]) + a * pm + (1 - a) * D * al[..., None]
            rep[card] = {k: [round(v, 2) for v in vals] for k, vals in L.items()}
            rep[card]['box'] = spec['box']
        report[i] = rep
        Image.fromarray(np.clip(np.round(out), 0, 255).astype(np.uint8)).save(os.path.join(out_dir, f'{i:03d}.png'))
    return report


if __name__ == '__main__':
    rep = main(sys.argv[1], sys.argv[2])
    json.dump({'timeline': {str(k): v for k, v in TL.items()}, 'exit_alpha': EXIT_ALPHA, 'pulse_fill': PULSE,
               'layout_per_frame': {str(k): v for k, v in rep.items() if v}},
              open(sys.argv[3], 'w'), indent=1, default=float)
    print('ok')
