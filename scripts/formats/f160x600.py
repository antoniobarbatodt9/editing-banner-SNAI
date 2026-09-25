"""Formato 160x600: timeline misurata sul master 00_master_approvato/SNAI_BonusSport_160x600_MASTER.mp4.

Stesse regole del 300x600: card nuove sempre >= card originali (+1 px), nessuno sfondo inventato,
pulse SNAI neutralizzato con i pixel originali dei frame di riposo 115 e 127, CTA invariata.
Il 160x600 non ha uscita: le card restano a schermo fino all'ultimo frame.
"""
import assets as A
SRC_NAME = 'SNAI_BonusSport_160x600'
RADIUS = 7.0
CARD_BORDER = (34., 35., 40.)
PULSE_SRC = (115, 127)

# ---------------------------------------------------------------- timeline (box esterni inclusivi x0,y0,x1,y1)
X0, X1 = 5, 155                                   # larghezza card SNAI originale (6-154) + 1 px
PH3 = {'bet365': (X0, 97, X1, 214), 'snai': (X0, 219, X1, 351), 'wh': (X0, 356, X1, 473)}
OLD_PH3 = {'bet365': (25, 110, 134, 214), 'snai': (6, 219, 154, 351), 'wh': (27, 367, 134, 472)}
TL = {}
def put(f, card, box, k, ca=1.0):
    TL.setdefault(f, {})[card] = dict(box=box, k=k, ca=ca)
K2 = 1.30                                         # scala contenuti fasi 1-2 (card 138 px)
# f51: rettangolo scuro d'ingresso WH senza contenuti -> resta originale
for f in range(52, 70): put(f, 'wh', (X0, 207, X1, 344), K2, {52: 0.23, 53: 0.63}.get(f, 1.0))
put(70, 'wh', (X0, 219, X1, 356), K2)
put(71, 'wh', (X0, 233, X1, 370), K2)
put(72, 'wh', (X0, 271, X1, 408), K2)             # f72: rettangolo d'ingresso bet365 resta originale
for f in range(73, 98):
    put(f, 'wh', (X0, 289, X1, 426), K2)
    put(f, 'bet365', (X0, 146, X1, 283), K2, {73: 0.23, 74: 0.63}.get(f, 1.0))
# transizione 2 -> 3 (f98-99): unione di (box originale + 1 px) e interpolazione monotona
for f, pb, pw, bb, bw in [(98, .32, .31, (130, 261), (310, 443)),
                          (99, .51, .64, (121, 248), (331, 456))]:
    put(f, 'bet365', (X0, bb[0], X1, bb[1]), K2 - (K2 - 1) * pb)
    put(f, 'wh', (X0, bw[0], X1, bw[1]), K2 - (K2 - 1) * pw)
# SNAI: f98-99 rettangolo scuro d'ingresso senza contenuti -> resta originale
put(100, 'bet365', (X0, 97, X1, 217), 1.0)        # f100: bet365 originale ancora 3 px piu' basso
for f in range(101, 136): put(f, 'bet365', PH3['bet365'], 1.0)
for f in range(100, 136):
    put(f, 'wh', PH3['wh'], 1.0)
    put(f, 'snai', PH3['snai'], 1.0, {100: 0.24}.get(f, 1.0))
# card SNAI pulsata originale (f116-126): zona da riportare allo sfondo originale
PULSE = {116: (0, 212, 159, 358), 117: (0, 205, 159, 364), 118: (0, 198, 159, 372), 119: (0, 207, 159, 363),
         120: (3, 215, 157, 354), 123: (2, 215, 158, 354), 124: (0, 209, 159, 360), 125: (0, 212, 159, 357),
         126: (0, 213, 159, 357)}

CONTENT = {'bet365': ('500€', A.WHITE), 'wh': ('105€', A.WHITE), 'snai': ('2.000€', A.ORANGE_AMOUNT)}
H_LOGO, H_FINO, H_AMT, G1, G2 = 20.0, 9.0, 34.0, 6.0, 2.0
NUDGE = {'snai': (-3, +3)}   # come nel 300x600 approvato: logo SNAI piu' su, FINO A + 2.000EUR piu' giu'

# QA
QA_CTA_ROWS = (478, 516)
QA_REST = (60, 85, 110)
QA_STAB = [('snai', 102, 115), ('snai', 127, 135), ('bet365', 75, 97), ('bet365', 101, 135),
           ('wh', 54, 69), ('wh', 73, 97), ('wh', 100, 135)]
QA_PULSE_ORIG = (115, 127)
QA_SHEETS = [((60, 85, 110), '01_riposo_per_fase', 'Fotogrammi di riposo: WH solo (f60), bet365+WH (f85), tre card (f110)', (0, 0, 160, 600), 1.0),
             ((114, 116, 117, 118, 119, 121, 124, 126, 128), '02_ex_pulse_SNAI_f116-126', 'Prima / durante / dopo il vecchio pulse SNAI (f116-126)', (0, 180, 160, 400), 1.0),
             ((52, 53, 56, 73, 74, 78, 100, 101, 104), '03_ingressi_senza_contatori', 'Ingressi: importi subito al valore finale (niente conteggio / niente 900->500)', (0, 90, 160, 480), 0.8),
             ((96, 97, 98, 99, 100, 101), '04_transizione_fase2_fase3', 'Transizione verso le tre card: le card nuove coprono sempre le originali', (0, 90, 160, 480), 0.8),
             ((130, 133, 135), '05_finale', 'Finale (nessuna uscita nel 160x600)', (0, 0, 160, 600), 1.0)]
