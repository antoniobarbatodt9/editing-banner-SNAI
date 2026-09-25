"""Formato 300x50 (orizzontale): timeline misurata sul master 00_master_approvato/SNAI_BonusSport_300x50_MASTER.mp4.

Regole approvate applicate: misure uniformi, conteggio originale, card SNAI senza pulse, CTA invariata.
 - card orizzontale (originale x 4-178, y 1-35) una alla volta; logo a sinistra, "FINO A" sopra la fine
   del logo, importo allineato a destra; CTA separata a destra (x 204-295) con il suo pulse, invariata;
 - card originali SEMITRASPARENTI (si vede la rete): card nuove OPACHE, come nel 320x480 approvato;
 - "FINO A" compare lettera per lettera dopo il conteggio (animazione originale, conservata);
 - pulse SNAI f120-127: contrazioni (f123-124) coperte dalla card a misura piena; espansioni
   (f120-122, f125-127) con fascia y 0-36, x 0-200 interpolata tra frame reali (119->123, 124->128);
 - uscite WH (f68-71) e bet365 (f90-93): opacita' stimata pixel per pixel. Durata 10,0 s (150 frame).
"""
import assets as A
SRC_NAME = 'SNAI_BonusSport_300x50'
RADIUS = 4.0
CARD_BORDER = (52., 53., 57.)
CARD_FILL = (21., 22., 28.)
PULSE_SRC = None

BOX = (3, 0, 179, 36)
X0, X1 = BOX[0], BOX[2]
PH3 = {'bet365': BOX, 'snai': BOX, 'wh': BOX}
OLD_PH3 = {c: (4, 1, 178, 35) for c in ('bet365', 'snai', 'wh')}
TL = {}
def put(f, card, box, k, ca=1.0):
    TL.setdefault(f, {})[card] = dict(box=box, k=k, ca=ca)
K2 = 1.0
for f in range(52, 72): put(f, 'wh', BOX, 1.0, {52: 0, 53: 0, 54: 0.09, 55: 0.27, 56: 0.49, 57: 0.83, 58: 0.96}.get(f, 1.0))
for f in range(74, 94): put(f, 'bet365', BOX, 1.0, {74: 0, 75: 0, 76: 0.11, 77: 0.31, 78: 0.66}.get(f, 1.0))
for f in range(97, 151): put(f, 'snai', BOX, 1.0, {97: 0, 98: 0, 99: 0, 100: 0.19, 101: 0.49, 102: 0.72}.get(f, 1.0))
UNMIX = {68: 64, 69: 64, 70: 64, 71: 64, 90: 86, 91: 86, 92: 86, 93: 86}
FINO_REVEAL = {f: {'wh': 0} for f in range(52, 60)}
FINO_REVEAL.update({60: {'wh': 0.65}, 61: {'wh': 0.72}})
FINO_REVEAL.update({f: {'bet365': 0} for f in range(74, 81)})
FINO_REVEAL.update({81: {'bet365': 0}, 82: {'bet365': 0.65}, 83: {'bet365': 0.72}})
FINO_REVEAL.update({f: {'snai': 0} for f in range(97, 105)})
FINO_REVEAL.update({105: {'snai': 0.6}, 106: {'snai': 0.72}, 107: {'snai': 0.72}})
PULSE = {f: (0, 0, 200, 36) for f in (120, 121, 122, 125, 126, 127)}
PULSE_BRIGHT_GUARD = True
PULSE_FLOW_ROWS = (0, 37)      # il disclaimer (y>=74) non entra nel calcolo del flusso
PULSE_FLOW = {120: (119, 123), 121: (119, 123), 122: (119, 123), 125: (124, 128), 126: (124, 128), 127: (124, 128)}

CONTENT = {'bet365': ('500€', A.WHITE), 'wh': ('105€', A.WHITE), 'snai': ('2.000€', A.ORANGE_AMOUNT)}
H_LOGO, H_FINO, H_AMT, G1, G2 = 16.0, 5.0, 22.0, 0.0, 0.0
LAYOUT_H = {'logo_right': 88, 'amt_right': 174, 'base': 28, 'fino_top': 7,
            'logo_right_card': {'snai': 83}}   # SNAI: come l'originale, per lasciare spazio al 2.000EUR
NUDGE = {}
CUT_DENOISE = True
CUT_CLEAN = True
CUT_XMIN = {'wh': 100, 'bet365': 100, 'snai': 85}

COUNT = {54: {'wh': None},   # 57EUR all'11%: illeggibile anche nell'originale
         55: {'wh': (55, 58)}, 56: {'wh': (56, 58)}, 57: {'wh': 57}, 58: {'wh': 58}, 59: {'wh': 59},
         76: {'bet365': (76, 79)}, 77: {'bet365': (77, 79)}, 78: {'bet365': 78}, 79: {'bet365': 79},
         80: {'bet365': 80}, 81: {'bet365': 81},
         100: {'snai': (100, 103)}, 101: {'snai': (101, 103)}, 102: {'snai': 102},
         103: {'snai': 103}, 104: {'snai': 104}}

# QA
QA_CTA_ROWS = (10, 30)   # (colonne intere: include anche la card)
QA_REST = (64, 86, 112)
QA_STAB = [('wh', 63, 67), ('bet365', 85, 89), ('snai', 108, 150)]
QA_PULSE_ORIG = (119, 128)
QA_SHEETS = [((64, 86, 112), '01_riposo_per_card', 'Fotogrammi di riposo: WH (f64), bet365 (f86), SNAI (f112)', (0, 0, 300, 50), 1.0),
             ((119, 120, 121, 122, 123, 124, 125, 126, 127, 128), '02_ex_pulse_SNAI_f120-127', 'Pulse SNAI eliminato: card ferma; f120-122 e f125-127 interpolati tra frame reali', (0, 0, 200, 40), 1.0),
             ((53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63), '03_ingressi_conteggio', 'WH: ingresso, conteggio e FINO A scritto lettera per lettera', (0, 0, 200, 40), 1.0),
             ((67, 68, 69, 70, 71, 89, 90, 91, 92, 93), '04_uscite', "Uscite WH e bet365: stessa dissolvenza dell'originale", (0, 0, 200, 40), 1.0),
             ((136, 139, 142, 150), '05_finale', 'Finale (pulse CTA originale invariato)', (0, 0, 300, 50), 1.0)]
