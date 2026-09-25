"""Formato 320x320: timeline misurata sul master 00_master_approvato/SNAI_BonusSport_320x320_MASTER.mp4.

Stessa struttura di 300x250 / 336x280 (regole approvate), timeline propria:
 - card una alla volta, stessa posizione e misura (originale 74-245 x 42-190, opaca); nessun titolo;
 - misure uniformi come il 336x280: logo 25, FINO A 11, importo 41 px;
 - conteggio originale ripristinato (valori intermedi ritagliati dai fotogrammi originali);
 - card SNAI SENZA pulse (f116-127): contrazioni (f121-122) coperte dalla card a misura piena; nelle
   espansioni (f116-120, f124-127) la fascia y 0-218 e' interpolata con flusso ottico tra frame reali
   (115->121 e 123->128). La CTA ha un proprio pulse (f137-144) che resta invariato;
 - uscite WH (f68-70) e bet365 (f88-91) in dissolvenza: opacita' della card stimata pixel per pixel;
 - f92: rimossa la card NetBet presente per errore nel master (1 frame), vedi sotto;
 - durata del master: 10,0 s (150 frame).
"""
import assets as A
SRC_NAME = 'SNAI_BonusSport_320x320'
RADIUS = 10.0
CARD_BORDER = (45., 46., 48.)
PULSE_SRC = None

X0, X1 = 73, 246
BOX = (X0, 41, X1, 191)
PH3 = {'bet365': BOX, 'snai': BOX, 'wh': BOX}
OLD_PH3 = {c: (74, 42, 245, 190) for c in ('bet365', 'snai', 'wh')}
TL = {}
def put(f, card, box, k, ca=1.0):
    TL.setdefault(f, {})[card] = dict(box=box, k=k, ca=ca)
K2 = 1.0
# f51-53 / f73-75 / f100-103: rettangolo d'ingresso (la card si forma sopra lo sfondo) -> originale
for f in range(54, 71): put(f, 'wh', BOX, 1.0, {54: 0.02, 55: 0.33, 56: 0.62}.get(f, 1.0))
for f in range(76, 92): put(f, 'bet365', BOX, 1.0, {76: 0.12, 77: 0.48, 78: 0.91}.get(f, 1.0))
for f in range(104, 151): put(f, 'snai', BOX, 1.0, {104: 0.12, 105: 0.22, 106: 0.53, 107: 0.85}.get(f, 1.0))
UNMIX = {68: 64, 69: 64, 70: 64, 88: 86, 89: 86, 90: 86, 91: 86}
PULSE = {f: (0, 0, 319, 218) for f in (116, 117, 118, 119, 120, 124, 125, 126, 127)}
PULSE_FLOW = {f: (115, 121) for f in (116, 117, 118, 119, 120)}
PULSE_FLOW.update({f: (123, 128) for f in (124, 125, 126, 127)})
# f92: nell'originale compare per 1 frame una card NetBet (brand non in campagna) al posto della bet365 in
# dissolvenza -> nel riquadro card si usano i pixel reali del frame 93 (senza card; bet365 gia' svanita a f91)
PULSE[92] = (66, 34, 254, 200); PULSE_FLOW[92] = (93, 93)
PULSE_KEEP = [(62, 216, 256, 261)]      # CTA (66-252 x 224-257) + 4 px

CONTENT = {'bet365': ('500€', A.WHITE), 'wh': ('105€', A.WHITE), 'snai': ('2.000€', A.ORANGE_AMOUNT)}
H_LOGO, H_FINO, H_AMT, G1, G2 = 25.0, 11.0, 41.0, 10.0, 6.0
NUDGE = {}
CUT_DENOISE = True       # ingresso SNAI: valori 925/1.050 visibili solo in frame a bassa opacita'

COUNT = {54: {'wh': (54, 57)}, 55: {'wh': (55, 57)}, 56: {'wh': (56, 57)}, 57: {'wh': 57}, 58: {'wh': 58}, 59: {'wh': 59},
         76: {'bet365': (76, 79)}, 77: {'bet365': (77, 79)}, 78: {'bet365': 78}, 79: {'bet365': 79},
         80: {'bet365': 80}, 81: {'bet365': 81},
         104: {'snai': (104, 107)}, 105: {'snai': (105, 107)}, 106: {'snai': (106, 107)}, 107: {'snai': 107},
         108: {'snai': 108}}

# QA
QA_CTA_ROWS = (215, 265)
QA_REST = (64, 86, 112)
QA_STAB = [('wh', 60, 67), ('bet365', 82, 87), ('snai', 109, 150)]
QA_PULSE_ORIG = (115, 128)
QA_SHEETS = [((89, 90, 91, 92, 93, 94), '07_f92_netbet_rimosso', 'f92: card NetBet del master (errore) rimossa: riquadro card = pixel reali del frame 93', (66, 34, 254, 200), 1.0),
             ((64, 86, 112), '01_riposo_per_card', 'Fotogrammi di riposo: WH (f64), bet365 (f86), SNAI (f112)', (0, 0, 320, 320), 1.0),
             ((115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128), '02_ex_pulse_SNAI_f116-127', 'Pulse SNAI eliminato: card ferma; f116-120 e f124-127 interpolati tra frame reali', (0, 0, 320, 265), 0.7),
             ((53, 54, 55, 56, 75, 76, 77, 78, 103, 104, 105, 106), '03_ingressi_conteggio', 'Ingressi: conteggio originale ripristinato, cifre alla nuova dimensione uniforme', (66, 34, 254, 200), 0.8),
             ((67, 68, 69, 70, 71, 87, 88, 89, 90, 91, 92), '04_uscite', "Uscite WH e bet365: stessa dissolvenza dell'originale", (66, 34, 254, 200), 0.8),
             ((136, 138, 140, 142, 150), '05_finale', 'Finale (pulse CTA originale invariato)', (0, 0, 320, 320), 0.8)]
