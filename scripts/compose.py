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
PULSE_FLOW = getattr(_cfg, 'PULSE_FLOW', {})      # {frame: (frame_reale_prima, frame_reale_dopo)} -> interpolazione con flusso ottico
UNMIX = getattr(_cfg, 'UNMIX', {})
COUNT = getattr(_cfg, 'COUNT', {})                # {frame: {card: frame_originale}} -> valore intermedio del conteggio                # {frame: frame_di_riposo} -> dissolvenza/glitch: opacita' stimata pixel per pixel

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



SRC_DIR = None
_cut_cache = {}
def _amount_mask(img, box, orange):
    import cv2
    x0, y0, x1, y1 = box
    ox, oy = max(0, x0 + 4), max(0, y0 + 4)
    sub = img[oy:y1 - 3, ox:x1 - 3]
    v = sub[..., 0] if orange else sub.min(-1)            # arancio: canale R; bianco: minimo dei canali
    if orange: v = np.where(sub[..., 2] < sub[..., 0] * 0.6, v, np.minimum(v, sub.mean(-1)))
    bg = np.median(v[v < np.percentile(v, 60)])
    m = (v - bg) > 0.35 * (np.percentile(v, 99.7) - bg)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8))
    comps = [(k, *st[k]) for k in range(1, n) if st[k][4] >= 4]
    Hm = max(c[4] for c in comps)
    tall = [c for c in comps if c[4] >= 0.45 * Hm]
    low = max(c[2] + c[4] for c in tall)                  # riga di testo piu' in basso = importo
    row = [c for c in tall if abs(c[2] + c[4] - low) <= 0.12 * Hm]
    eur = max(row, key=lambda c: c[1] + c[3])             # il suo carattere piu' a destra = simbolo EUR
    H = eur[4]; base = eur[2] + eur[4]
    keep = [c for c in comps if abs(c[2] + c[4] - base) <= max(2, 0.08 * H) and c[1] + c[3] <= eur[1] + eur[3] + 1]
    km = np.isin(lab, [c[0] for c in keep]); km[:max(0, base - H - 1)] = False   # via "FINO A" attaccato sopra
    ys, xs = np.where(km)
    return v, bg, (xs.min() + ox, base - H + oy, xs.max() + ox, base - 1 + oy)


def cut_amount(src_frame, card, ref_frame=None):
    """Ritaglia l'importo intermedio del conteggio dal fotogramma ORIGINALE in cui compare (stesso font
    del video: le cifre 3,4,6,7,8,9 non esistono tra gli asset forniti). Nei frame in dissolvenza la
    posizione del numero si prende da un frame vicino ben leggibile (ref_frame). Restituisce un asset
    come _asset(): copertura stimata sul fondo della card, colore = colore campionato del master."""
    key = (src_frame, card, ref_frame)
    if key in _cut_cache: return _cut_cache[key]
    load = lambda f: np.array(Image.open(os.path.join(SRC_DIR, f'{f:03d}.png')).convert('RGB')).astype(float)
    orange = card == 'snai'
    img = load(src_frame)
    if ref_frame is None:
        _, _, bb = _amount_mask(img, TL[src_frame][card]['box'], orange)
    else:
        _, _, bb = _amount_mask(load(ref_frame), TL[ref_frame][card]['box'], orange)
        bb = (bb[0] - 6, bb[1] - 1, bb[2] + 6, bb[3] + 1)
    x0, y0, x1, y1 = bb
    sub = img[y0:y1 + 1, x0:x1 + 1]
    v = sub[..., 0] if orange else sub.min(-1)
    if orange: v = np.where(sub[..., 2] < sub[..., 0] * 0.6, v, np.minimum(v, sub.mean(-1)))
    x0c, y0c, x1c, y1c = TL[src_frame][card]['box']
    card_px = img[y0c + 4:y1c - 3, x0c + 4:x1c - 3]
    cv_ = card_px[..., 0] if orange else card_px.min(-1)
    bg = np.median(cv_[cv_ < np.percentile(cv_, 60)])
    peak = np.percentile(v, 97)
    a = np.clip((v - bg) / max(peak - bg, 1), 0, 1)
    a = np.where(a < 0.08, 0, a)
    col = A.ORANGE_AMOUNT if orange else A.WHITE
    res = _asset(np.broadcast_to(np.array(col, float), a.shape + (3,)).copy(), a)
    res['h'] = y1 - y0 + 1 if ref_frame is None else y1 - y0 - 1      # altezza d'inchiostro = altezza del simbolo EUR
    res['top'] = 0 if ref_frame is None else 1
    _cut_cache[key] = res
    return res


def render_card(card, spec, frame=None):
    box, k, ca = spec['box'], spec['k'], spec['ca']
    region = (box[0] - 2, box[1] - 2, box[2] + 2, box[3] + 2)
    pm, al, _ = card_layer(box, k, ca, region)
    L = layout(card, box, k)
    ox, oy = region[0], region[1]
    x, y, h, _ = L['logo']; place(pm, al, ('logo', card), _logo[card], x, y, h, ox, oy, ca)
    x, y, h = L['fino']; place(pm, al, ('fino',), _fino, x, y, h, ox, oy, ca)
    x, y, h, aw = L['amount']
    if frame in COUNT and card in COUNT[frame]:
        # valore intermedio: stessa altezza e stesso centro del valore finale, "FINO A" fermo
        src = COUNT[frame][card]; ref = None
        if isinstance(src, tuple): src, ref = src
        ast = cut_amount(src, card, ref)
        w2 = ast['w'] * h / ast['h']
        place(pm, al, ('cut', src, card), ast, x + aw / 2 - w2 / 2, y, h, ox, oy, ca)
        L = dict(L); L['amount'] = (x + aw / 2 - w2 / 2, y, h, w2)
    else:
        place(pm, al, ('amt', card), _amt[card], x, y, h, ox, oy, ca)
    Hh, Ww = al.shape
    pm_d = pm.reshape(Hh // S, S, Ww // S, S, 3).mean((1, 3))
    al_d = al.reshape(Hh // S, S, Ww // S, S).mean((1, 3))
    return region, pm_d, al_d, L



def flow_interp(A, B, t):
    """frame intermedio tra due frame REALI A e B (t in 0..1) con flusso ottico bidirezionale (DIS)."""
    import cv2
    ga = cv2.cvtColor(A.astype(np.uint8), cv2.COLOR_RGB2GRAY); gb = cv2.cvtColor(B.astype(np.uint8), cv2.COLOR_RGB2GRAY)
    dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
    fab = dis.calc(ga, gb, None); fba = dis.calc(gb, ga, None)
    h, w = ga.shape; X, Y = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    wa = cv2.remap(A.astype(np.float32), X - t * fab[..., 0], Y - t * fab[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    wb = cv2.remap(B.astype(np.float32), X - (1 - t) * fba[..., 0], Y - (1 - t) * fba[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return (1 - t) * wa + t * wb


def local_opacity(orig, rest, win=15):
    """opacita' locale della card originale: regressione passa-alto (orig vs frame di riposo) su finestre."""
    from scipy.ndimage import gaussian_filter, uniform_filter
    o = orig.mean(-1); r = rest.mean(-1)
    ho = o - gaussian_filter(o, 2); hr = r - gaussian_filter(r, 2)
    num = uniform_filter(ho * hr, win); den = uniform_filter(hr * hr, win)
    k = np.where(den > 4, num / np.maximum(den, 1e-6), np.nan)
    # dove non c'e' testo per stimare, prende la mediana delle finestre valide vicine
    valid = ~np.isnan(k)
    kg = np.nanmedian(k) if valid.any() else 0.0
    kf = np.where(valid, k, kg)
    w = uniform_filter(valid.astype(float), 41); kk = uniform_filter(np.where(valid, k, 0), 41)
    kf = np.where(valid, k, np.where(w > 0.05, kk / np.maximum(w, 1e-6), kg))
    return np.clip(gaussian_filter(kf, 2), 0, 1)


def main(src_dir, out_dir):
    global SRC_DIR; SRC_DIR = src_dir
    os.makedirs(out_dir, exist_ok=True)
    load = lambda i: np.array(Image.open(os.path.join(src_dir, f'{i:03d}.png')).convert('RGB')).astype(float)
    n = len([f for f in os.listdir(src_dir) if f.endswith('.png')])
    p0, p1 = PULSE_SRC if PULSE_SRC else (1, 1); f81, f93 = load(p0), load(p1)
    report = {}
    for i in range(1, n + 1):
        orig = load(i); out = orig.copy()
        PAD = 24; H0, W0 = orig.shape[:2]
        origp = np.pad(orig, ((PAD, PAD), (PAD, PAD), (0, 0)), mode='edge')
        if i in PULSE and i in PULSE_FLOW:
            fa, fb = PULSE_FLOW[i]; x0, y0, x1, y1 = PULSE[i]
            I = flow_interp(load(fa), load(fb), (i - fa) / (fb - fa))
            out[y0:y1 + 1, x0:x1 + 1] = I[y0:y1 + 1, x0:x1 + 1]
        elif i in PULSE:
            x0, y0, x1, y1 = PULSE[i]; w = (i - p0) / (p1 - p0)
            out[y0:y1 + 1, x0:x1 + 1] = (1 - w) * f81[y0:y1 + 1, x0:x1 + 1] + w * f93[y0:y1 + 1, x0:x1 + 1]
        a = EXIT_ALPHA.get(i, 1.0)
        rep = {}
        for card, spec in TL.get(i, {}).items():
            region, pm, al, L = render_card(card, spec, i)
            rx0, ry0, rx1, ry1 = region
            if rx0 < 0 or ry0 < 0 or rx1 >= W0 or ry1 >= H0:
                # card oltre il bordo del banner: compone su tela estesa e ritaglia
                outp = np.pad(out, ((PAD, PAD), (PAD, PAD), (0, 0)), mode='edge')
                slp = (slice(ry0 + PAD, ry1 + PAD + 1), slice(rx0 + PAD, rx1 + PAD + 1))
                outp[slp] = outp[slp] * (1 - al[..., None]) + pm
                out = outp[PAD:PAD + H0, PAD:PAD + W0]
                rep[card] = {k: [round(v, 2) for v in vals] for k, vals in L.items()}; rep[card]['box'] = spec['box']
                continue
            sl = (slice(ry0, ry1 + 1), slice(rx0, rx1 + 1))
            if i in UNMIX:
                # dissolvenza/glitch d'uscita: contenuto finale identico al riposo -> si toglie la card
                # originale con la sua opacita' locale e si mette la nuova con la stessa opacita'
                R = load(UNMIX[i])[sl]
                km = local_opacity(orig[sl], R)[..., None]
                Knew = R * (1 - al[..., None]) + pm                    # card nuova composta sul riposo
                out[sl] = orig[sl] + km * (Knew - R)
            elif a >= 1.0:
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
