"""Formato 320x480: timeline misurata sul master 00_master_approvato/SNAI_BonusSport_320x480_MASTER.mp4.

Differenze rispetto agli altri formati (decisioni del cliente: A + P1 + importi 57 px):
 - le tre card compaiono UNA ALLA VOLTA, nella stessa posizione e con la stessa misura;
 - le card originali sono leggermente semitrasparenti (si intravede la rete): le card nuove sono
   OPACHE, perche' sotto le vecchie scritte non esiste alcun dato di sfondo da ricostruire (A);
 - il pulse SNAI (f90-99) copre sfondo in movimento: l'anello viene ricostruito interpolando con
   flusso ottico i frame REALI in cui e' visibile (89->93 e 95->99) (P1);
 - uscite WH (f52-53) e bet365 (f68-69, glitch a blocchi): opacita' della card stimata pixel per pixel;
 - durata del master: 7,87 s (118 frame).
"""
import assets as A
SRC_NAME = 'SNAI_BonusSport_320x480'
RADIUS = 12.0
CARD_BORDER = (49., 48., 52.)
PULSE_SRC = None

# ---------------------------------------------------------------- timeline (box esterni inclusivi x0,y0,x1,y1)
X0, X1 = 29, 290
BOX = (X0, 105, X1, 332)                 # card originale a riposo (30-289 x 106-331) + 1 px
PH3 = {'bet365': BOX, 'snai': BOX, 'wh': BOX}
OLD_PH3 = {'bet365': (30, 106, 289, 331), 'snai': (30, 106, 289, 331), 'wh': (30, 106, 289, 331)}
TL = {}
def put(f, card, box, k, ca=1.0):
    TL.setdefault(f, {})[card] = dict(box=box, k=k, ca=ca)
K2 = 1.0
# WH: f41-42 rettangolo d'ingresso senza contenuti leggibili -> originale
for f in range(43, 54): put(f, 'wh', BOX, 1.0, {43: 0.72}.get(f, 1.0))
# bet365: f57-58 rettangolo d'ingresso -> originale
for f in range(59, 70): put(f, 'bet365', BOX, 1.0, {59: 0.11, 60: 0.74}.get(f, 1.0))
# SNAI: f76-79 ingresso (card non ancora formata, contenuto <20%) -> originale
for f in range(80, 116): put(f, 'snai', BOX, 1.0, {80: 0.64}.get(f, 1.0))
UNMIX = {52: 49, 53: 49, 68: 65, 69: 65}  # uscite: frame -> frame di riposo della stessa card
# pulse SNAI: zona coperta dalla card ingrandita (bordi misurati + 3 px), ricostruita con flusso ottico
PULSE = {90: (17, 95, 302, 342), 91: (0, 72, 319, 364), 92: (0, 72, 319, 364),
         96: (17, 95, 301, 342), 97: (18, 96, 301, 341), 98: (25, 101, 294, 335)}
PULSE_FLOW = {90: (89, 93), 91: (89, 93), 92: (89, 93), 96: (95, 99), 97: (95, 99), 98: (95, 99)}

CONTENT = {'bet365': ('500€', A.WHITE), 'wh': ('105€', A.WHITE), 'snai': ('2.000€', A.ORANGE_AMOUNT)}
H_LOGO, H_FINO, H_AMT, G1, G2 = 41.0, 16.0, 57.0, 17.0, 7.0
NUDGE = {}                               # card tutte uguali: nessun ritocco specifico SNAI

# QA
QA_CTA_ROWS = (360, 414)
QA_REST = (49, 65, 85)
QA_STAB = [('wh', 44, 51), ('bet365', 61, 67), ('snai', 81, 89), ('snai', 100, 115)]
QA_PULSE_ORIG = (89, 100)
QA_SHEETS = [((49, 65, 85), '01_riposo_per_card', 'Fotogrammi di riposo: WH (f49), bet365 (f65), SNAI (f85)', (0, 0, 320, 480), 1.0),
             ((89, 90, 91, 92, 93, 95, 96, 97, 98, 99), '02_ex_pulse_SNAI_f90-99', 'Prima / durante / dopo il vecchio pulse SNAI (f90-99)', (0, 60, 320, 380), 0.8),
             ((42, 43, 44, 58, 59, 60, 61, 79, 80, 81), '03_ingressi_senza_contatori', 'Ingressi: importi subito al valore finale', (0, 90, 320, 350), 0.6),
             ((51, 52, 53, 54, 67, 68, 69, 70), '04_uscite', 'Uscite WH e bet365: stessa dissolvenza/glitch dell\'originale', (0, 90, 320, 350), 0.6),
             ((114, 115, 116, 117, 118), '05_finale', 'Finale', (0, 0, 320, 480), 0.8)]
