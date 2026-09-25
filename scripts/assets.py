"""Prepara gli asset (maschere alpha ad alta risoluzione + colore) per il compositing.

Tutti i colori sono espressi nello spazio RGB decodificato del master
(00_master_approvato/SNAI_BonusSport_300x600_MASTER_2000.mp4), che ha il nero a ~16
e il bianco a ~235: i colori sono campionati dal master stesso.
"""
import os
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OFF = os.path.join(ROOT, '01_originali_ufficiali')

# colori campionati dal master (frame 100, pixel pieni dei testi)
WHITE = np.array([234., 234., 236.])
ORANGE_AMOUNT = np.array([254., 109., 9.])
CARD_FILL = np.array([19., 20., 24.])
CARD_BORDER = np.array([47., 48., 52.])


def _crop_ink(alpha, thr=0.02):
    ys, xs = np.where(alpha > thr)
    return alpha[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def _to_master_colors(rgb):
    """Porta i colori di un file ufficiale nella resa del master: i neutri vengono
    compressi come nel master (bianco -> ~235), i colori saturi restano invariati
    (come l'arancio dell'importo SNAI, identico nei due export)."""
    rgb = rgb.astype(float)
    mx = rgb.max(-1, keepdims=True); mn = rgb.min(-1, keepdims=True)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    squeezed = 16 + rgb * 219 / 255
    return rgb * sat + squeezed * (1 - sat)


def load_logo(name):
    """Restituisce (rgb HxWx3, alpha HxW) croppati sull'inchiostro, risoluzione nativa."""
    if name == 'snai':
        im = np.array(Image.open(os.path.join(OFF, 'asset_video_SPORT', 'logo_snai.png')).convert('RGBA')).astype(float)
        a = im[..., 3] / 255; rgb = _to_master_colors(im[..., :3])
    elif name == 'wh':
        im = np.array(Image.open(os.path.join(OFF, 'asset_video_SPORT', 'WilliamHill white.png')).convert('RGBA')).astype(float)
        a = im[..., 3] / 255; rgb = np.broadcast_to(WHITE, im.shape[:2] + (3,)).copy()
    elif name == 'bet365':
        # file ufficiale: scritta bianca su riquadro nero -> la luminanza della scritta e' la copertura
        im = np.array(Image.open(os.path.join(OFF, 'asset_video_SPORT', 'bet365 white.png')).convert('RGBA')).astype(float)
        box = im[..., 3] > 250
        ys, xs = np.where(box)
        y0, y1, x0, x1 = ys.min() + 6, ys.max() - 6, xs.min() + 6, xs.max() - 6   # interno del riquadro nero
        lum = im[y0:y1, x0:x1, :3].mean(-1) / 255
        a = np.clip((lum - 0.02) / 0.96, 0, 1); rgb = np.broadcast_to(WHITE, a.shape + (3,)).copy()
        im = None
    else:
        raise ValueError(name)
    ys, xs = np.where(a > 0.02)
    sl = (slice(ys.min(), ys.max() + 1), slice(xs.min(), xs.max() + 1))
    return rgb[sl], a[sl]


def load_fino_a():
    im = np.array(Image.open(os.path.join(OFF, 'asset_video_SPORT', 'text_fino_a.png')).convert('LA')).astype(float)
    a = im[..., 1] / 255
    a = _crop_ink(a)
    return np.broadcast_to(WHITE, a.shape + (3,)).copy(), a


AMOUNT_FILES = {'500€': 'text_500.png', '105€': 'text_105.png', '2.000€': 'text_2000.png'}
def render_amount(text, color):
    """Importo dall'asset estratto dal video (font originale): si usa la sola copertura (alpha),
    il colore e' quello campionato dal master."""
    im = np.array(Image.open(os.path.join(OFF, 'asset_video_SPORT', AMOUNT_FILES[text])).convert('RGBA')).astype(float)
    a = _crop_ink(im[..., 3] / 255)
    return np.broadcast_to(np.array(color, float), a.shape + (3,)).copy(), a


def resize_rgba(rgb, a, h, w):
    """Ridimensiona in premoltiplicato (niente aloni)."""
    pm = np.dstack([rgb * a[..., None], a])
    out = []
    for c in range(4):
        out.append(np.array(Image.fromarray(pm[..., c].astype(np.float32), 'F').resize((w, h), Image.LANCZOS)))
    out = np.dstack(out)
    al = np.clip(out[..., 3], 0, 1)
    col = np.where(al[..., None] > 1e-4, out[..., :3] / np.maximum(al[..., None], 1e-4), 0)
    return np.clip(col, 0, 255), al


if __name__ == '__main__':
    os.makedirs(os.path.join(ROOT, '06_loghi'), exist_ok=True)
    for n in ['snai', 'wh', 'bet365']:
        rgb, a = load_logo(n)
        Image.fromarray(np.dstack([rgb, a * 255]).clip(0, 255).astype(np.uint8), 'RGBA').save(
            os.path.join(ROOT, '06_loghi', f'logo_{n}_mastercolor.png'))
        print(n, 'ink', a.shape, 'aspect', round(a.shape[1] / a.shape[0], 4))
    rgb, a = load_fino_a(); print('fino a', a.shape, 'aspect', round(a.shape[1] / a.shape[0], 4))
    for t in ['500€', '2.000€', '105€']:
        rgb, a = render_amount(t, WHITE)
        print(t, a.shape, 'aspect', round(a.shape[1] / a.shape[0], 4), 'width@39px', round(39 * a.shape[1] / a.shape[0], 1))
