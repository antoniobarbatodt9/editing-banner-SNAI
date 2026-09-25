"""Formato 300x250: timeline misurata sul master 00_master_approvato/SNAI_BonusSport_300x250_MASTER.mp4.

Stessa struttura del 320x480 (regole del cliente gia' approvate):
 - le tre card compaiono UNA ALLA VOLTA, nella stessa posizione e misura (card originale 73-226 x 23-155,
   opaca: nessuna trasparenza da gestire); nessun titolo in questo formato;
 - misure uniformi: logo 22 px (= William Hill originale), FINO A 10 px, importo 37 px
   ("2.000EUR" originale 144 px su card da 154 -> 131 px, margine ~11 px per lato);
 - conteggio originale ripristinato (valori intermedi ritagliati dai fotogrammi originali);
 - card SNAI SENZA pulse (f116-126): contrazioni (f120-122) coperte dalla card a misura piena; nelle
   espansioni (f116-119, f123-126) la fascia y 0-212 e' interpolata con flusso ottico tra frame reali
   (115->120 e 122->127); la CTA "SCOPRI DI PIU'" resta sempre il pixel reale del frame;
 - uscite WH (f67-69) e bet365 (f90-92) in dissolvenza: opacita' della card stimata pixel per pixel;
 - durata del master: 10,0 s (150 frame).
"""
import assets as A
SRC_NAME = 'SNAI_BonusSport_300x250'
RADIUS = 9.0
CARD_BORDER = (44., 45., 47.)
PULSE_SRC = None

X0, X1 = 72, 227
BOX = (X0, 22, X1, 156)
PH3 = {'bet365': BOX, 'snai': BOX, 'wh': BOX}
OLD_PH3 = {c: (73, 23, 226, 155) for c in ('bet365', 'snai', 'wh')}
TL = {}
def put(f, card, box, k, ca=1.0):
    TL.setdefault(f, {})[card] = dict(box=box, k=k, ca=ca)
K2 = 1.0
# WH: f51 rettangolo d'ingresso vuoto -> originale; contenuto in dissolvenza f52-53
for f in range(52, 70): put(f, 'wh', BOX, 1.0, {52: 0.10, 53: 0.30, 54: 0.85}.get(f, 1.0))
# bet365: f73 rettangolo vuoto -> originale
for f in range(74, 93): put(f, 'bet365', BOX, 1.0, {74: 0.09, 75: 0.30, 76: 0.83}.get(f, 1.0))
# SNAI: f100-101 rettangolo vuoto -> originale
for f in range(102, 151): put(f, 'snai', BOX, 1.0, {102: 0.06, 103: 0.42, 104: 0.89}.get(f, 1.0))
UNMIX = {67: 60, 68: 60, 69: 60, 90: 85, 91: 85, 92: 85}
PULSE = {f: (0, 0, 299, 212) for f in (116, 117, 118, 119, 123, 124, 125, 126)}
PULSE_FLOW = {116: (115, 120), 117: (115, 120), 118: (115, 120), 119: (115, 120),
              123: (122, 127), 124: (122, 127), 125: (122, 127), 126: (122, 127)}
PULSE_KEEP = [(62, 170, 236, 207)]      # CTA (66-232 x 174-203) + 4 px

CONTENT = {'bet365': ('500€', A.WHITE), 'wh': ('105€', A.WHITE), 'snai': ('2.000€', A.ORANGE_AMOUNT)}
H_LOGO, H_FINO, H_AMT, G1, G2 = 22.0, 10.0, 37.0, 9.0, 5.0
NUDGE = {}

# conteggio originale (valore intermedio ritagliato dal fotogramma originale indicato; (f, rif) = dissolvenza)
COUNT = {52: {'wh': (52, 55)}, 53: {'wh': (53, 55)}, 54: {'wh': (54, 55)}, 55: {'wh': 55}, 56: {'wh': 56},
         57: {'wh': 57}, 58: {'wh': 58},
         74: {'bet365': (74, 77)}, 75: {'bet365': (75, 77)}, 76: {'bet365': (76, 77)}, 77: {'bet365': 77},
         78: {'bet365': 78}, 79: {'bet365': 79}, 80: {'bet365': 80},
         102: {'snai': (102, 105)}, 103: {'snai': (103, 105)}, 104: {'snai': (104, 105)}, 105: {'snai': 105},
         106: {'snai': 106}, 107: {'snai': 107}}

# QA
QA_CTA_ROWS = (168, 210)
QA_REST = (60, 85, 112)
QA_STAB = [('wh', 59, 66), ('bet365', 81, 89), ('snai', 108, 150)]
QA_PULSE_ORIG = (115, 127)
QA_SHEETS = [((60, 85, 112), '01_riposo_per_card', 'Fotogrammi di riposo: WH (f60), bet365 (f85), SNAI (f112)', (0, 0, 300, 250), 1.0),
             ((115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127), '02_ex_pulse_SNAI_f116-126', 'Pulse SNAI eliminato: card ferma; f116-119 e f123-126 interpolati tra frame reali', (0, 0, 300, 215), 0.8),
             ((51, 52, 53, 54, 73, 74, 75, 76, 101, 102, 103, 104), '03_ingressi_conteggio', 'Ingressi: conteggio originale ripristinato, cifre alla nuova dimensione uniforme', (60, 15, 240, 165), 0.8),
             ((66, 67, 68, 69, 70, 89, 90, 91, 92, 93), '04_uscite', "Uscite WH e bet365: stessa dissolvenza dell'originale", (60, 15, 240, 165), 0.8),
             ((140, 145, 150), '05_finale', 'Finale', (0, 0, 300, 250), 1.0)]
