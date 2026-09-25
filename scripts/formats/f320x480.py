"""Formato 320x480: timeline misurata sul master 00_master_approvato/SNAI_BonusSport_320x480_MASTER.mp4.

Differenze rispetto agli altri formati (decisioni del cliente: A + P1 + importi 57 px):
 - le tre card compaiono UNA ALLA VOLTA, nella stessa posizione e con la stessa misura;
 - le card originali sono leggermente semitrasparenti (si intravede la rete): le card nuove sono
   OPACHE, perche' sotto le vecchie scritte non esiste alcun dato di sfondo da ricostruire (A);
 - il pulse SNAI (f90-99) e' eliminato del tutto (v5, richiesta del cliente): card sempre a riposo;
   nei frame di espansione f90-92 e f96-98 l'intero fotogramma e' interpolato tra frame reali;
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
# pulse SNAI: il cliente chiede che la card SNAI NON pulsi mai (v5).
#  - contrazioni (f93-95, f99): card a misura piena, copre gia' l'originale -> nessuna ricostruzione;
#  - espansioni (f90-92, f96-98): la card resta a misura di riposo; lo sfondo che la card originale
#    ingrandita copriva non esiste in nessun frame -> l'intera fascia tra titolo e CTA (tutta la larghezza)
#    e' interpolata con flusso ottico tra i frame reali 89->93 e 95->99, con bordo sfumato; titolo, CTA e
#    disclaimer restano i pixel reali del frame.
#    Dichiarato come sfondo ricostruito (inferred) nel report.
PULSE = {f: (0, 64, 319, 366) for f in (90, 91, 92, 96, 97, 98)}   # fascia tra titolo e CTA
PULSE_FLOW = {90: (89, 93), 91: (89, 93), 92: (89, 93), 96: (95, 99), 97: (95, 99), 98: (95, 99)}

CONTENT = {'bet365': ('500€', A.WHITE), 'wh': ('105€', A.WHITE), 'snai': ('2.000€', A.ORANGE_AMOUNT)}
H_LOGO, H_FINO, H_AMT, G1, G2 = 41.0, 16.0, 57.0, 17.0, 7.0
NUDGE = {}                               # card tutte uguali: nessun ritocco specifico SNAI

# conteggio originale degli importi (valore intermedio ritagliato dal fotogramma originale indicato)
COUNT = {43: {'wh': 43}, 44: {'wh': 44}, 45: {'wh': 45}, 46: {'wh': 46},
         59: {'bet365': 60}, 60: {'bet365': 60}, 61: {'bet365': 61}, 62: {'bet365': 62},
         80: {'snai': 80}, 81: {'snai': 81}, 82: {'snai': 82}, 83: {'snai': 83}}

# QA
QA_CTA_ROWS = (360, 414)
QA_REST = (49, 65, 85)
QA_STAB = [('wh', 47, 51), ('bet365', 63, 67), ('snai', 84, 115)]   # dal termine del conteggio all'uscita
QA_PULSE_ORIG = (89, 100)
QA_SHEETS = [((49, 65, 85), '01_riposo_per_card', 'Fotogrammi di riposo: WH (f49), bet365 (f65), SNAI (f85)', (0, 0, 320, 480), 1.0),
             ((89, 90, 91, 92, 93, 95, 96, 97, 98, 99), '02_ex_pulse_SNAI_f90-99', 'Pulse SNAI eliminato: card ferma; f90-92 e f96-98 interpolati tra frame reali', (0, 60, 320, 380), 0.8),
             ((42, 43, 44, 58, 59, 60, 61, 79, 80, 81), '03_ingressi_conteggio', 'Ingressi: conteggio originale ripristinato, cifre alla nuova dimensione uniforme', (0, 90, 320, 350), 0.6),
             ((51, 52, 53, 54, 67, 68, 69, 70), '04_uscite', 'Uscite WH e bet365: stessa dissolvenza/glitch dell\'originale', (0, 90, 320, 350), 0.6),
             ((114, 115, 116, 117, 118), '05_finale', 'Finale', (0, 0, 320, 480), 0.8)]
