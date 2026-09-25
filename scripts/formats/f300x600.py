"""Formato 300x600: timeline misurata sul master 2.000 EUR (vedi REPORT_300x600.md)."""
import assets as A
SRC_NAME = 'SNAI_BonusSport_300x600'
RADIUS = 11.0
CARD_BORDER = (47., 48., 52.)
PULSE_SRC = (81, 93)          # frame di riposo da cui prendere lo sfondo originale per l'anello del pulse
# ---------------------------------------------------------------- timeline (box esterni inclusivi x0,y0,x1,y1)
X0, X1 = 64, 237
PH3 = {'bet365': (X0, 71, X1, 201), 'snai': (X0, 208, X1, 361), 'wh': (X0, 368, X1, 498)}
OLD_PH3 = {'bet365': (87, 79, 213, 200), 'snai': (65, 209, 236, 360), 'wh': (86, 379, 214, 488)}
TL = {}
def put(f, card, box, k, ca=1.0):
    TL.setdefault(f, {})[card] = dict(box=box, k=k, ca=ca)
K2 = 1.31                                                   # scala contenuti fasi 1-2 (card 152 px)
# box misurati sul master 2.000 EUR (i frame NON coincidono 1:1 con il file 1.500 EUR)
for f in range(43, 51): put(f, 'wh', (X0, 191, X1, 342), K2)
put(51, 'wh', (X0, 232, X1, 383), K2)
for f in range(52, 64):
    put(f, 'wh', (X0, 286, X1, 437), K2)
    put(f, 'bet365', (X0, 123, X1, 274), K2, {52: 0.25, 53: 0.67}.get(f, 1.0))
# transizione 2 -> 3: box = unione di (box originale + 1 px) e interpolazione monotona fase2 -> fase3
for f, pb, pw, bb, bw in [(64, .269, .221, (109, 255), (304, 451)),
                          (65, .782, .697, (82, 218), (343, 480)),
                          (66, .933, .841, (74, 206), (355, 489))]:
    put(f, 'bet365', (X0, bb[0], X1, bb[1]), K2 - (K2 - 1) * pb)
    put(f, 'wh', (X0, bw[0], X1, bw[1]), K2 - (K2 - 1) * pw)
# SNAI: f65 resta originale (rettangolo scuro d'ingresso, senza contenuti);
# f66 ingresso in scala verticale come nell'originale, contenuto in dissolvenza
put(66, 'snai', (X0, 214, X1, 347), 0.86, 0.15)
for f in range(67, 127):
    put(f, 'bet365', PH3['bet365'], 1.0)
    put(f, 'wh', PH3['wh'], 1.0)
    put(f, 'snai', PH3['snai'], 1.0, {67: 0.63}.get(f, 1.0))
EXIT_ALPHA = {124: 0.951, 125: 0.52, 126: 0.262}   # regressione passa-alto sui contenuti
# card SNAI pulsata originale: bordi misurati + 4 px, solo dove esce dalla card nuova
PULSE = {82: (51, 197, 249, 372), 83: (37, 184, 264, 385), 84: (39, 185, 260, 381), 85: (57, 200, 243, 367),
         89: (54, 199, 246, 369), 90: (55, 200, 245, 368), 91: (58, 202, 243, 366), 92: (61, 205, 240, 363)}

CONTENT = {'bet365': ('500€', A.WHITE), 'wh': ('105€', A.WHITE), 'snai': ('2.000€', A.ORANGE_AMOUNT)}
H_LOGO, H_FINO, H_AMT, G1, G2 = 21.0, 10.0, 39.0, 8.0, 3.0
NUDGE = {'snai': (-4, +4)}   # SNAI: logo 4 px piu' su, FINO A + 2.000EUR 4 px piu' giu'


# QA
QA_CTA_ROWS = (505, 548)
QA_REST = (47, 60, 100)
QA_STAB = [('snai', 68, 123), ('bet365', 54, 63), ('bet365', 67, 123), ('wh', 43, 50), ('wh', 52, 63), ('wh', 67, 123)]
QA_PULSE_ORIG = (81, 93)
QA_SHEETS = [((47, 60, 100), '01_riposo_per_fase', 'Fotogrammi di riposo: WH solo (f47), bet365+WH (f60), tre card (f100)', (0, 0, 300, 600), 1.0),
             ((80, 82, 83, 84, 86, 87, 89, 91, 93), '02_ex_pulse_SNAI_f80-93', 'Prima / durante / dopo il vecchio pulse SNAI (f82-92)', (20, 160, 280, 400), 1.0),
             ((43, 44, 46, 52, 53, 54, 66, 67, 68, 76), '03_ingressi_senza_contatori', 'Ingressi: importi subito al valore finale (niente conteggio / niente 900->500)', (40, 100, 260, 500), 0.8),
             ((62, 63, 64, 65, 66, 67, 70), '04_transizione_fase2_fase3', 'Transizione verso le tre card: le card nuove coprono sempre le originali', (40, 60, 260, 520), 0.8),
             ((122, 123, 124, 125, 126, 127), '05_uscita', "Uscita: stessa curva di dissolvenza misurata sull'originale (a=0.95/0.52/0.26)", (40, 60, 260, 520), 0.8)]
