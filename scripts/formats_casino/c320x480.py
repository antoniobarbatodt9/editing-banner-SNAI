"""Bonus Casino' 320x480 - timeline misurata su 00_master_approvato/casino/SNAI_BonusCasino_320x480_MASTER.mp4 (14 s, 210 frame).

 f1-52   sigla: BONUS CASINO' + esplosione simboli slot (originale, non toccata)
 f53-68  conteggio NetBet al centro (originale)          f69 frame vuoto (glitch originale)
 f70-82  NetBet si assesta e resta (fase 1: FINO A 13 / importo 51 originali; logo ufficiale 22 px da f74)
 f83-98  conteggio GoldBet (originale)                  f99-100 comparsa GoldBet (originale)
 f101-109 fase 2: GoldBet+NetBet - logo GoldBet 24 -> 22 px, logo NetBet ufficiale 22 px
 f110    frame vuoto (glitch originale)
 f111-116 riordino della pila (ricalcolato con la curva originale verso le misure finali uniformi)
 f116-129 conteggio SNAI al centro (originale)          f130-133 comparsa logo/FINO A SNAI (ricalcolata)
 f134    glitch originale: SNAI assente                  f135-187 riposo; pulse SNAI f145-156 ELIMINATO
 f162-179 pulse CTA (originale, invariato)               f188-210 esplosione di chiusura (simboli originali)
"""
WHITE = (254., 254., 255.)
ORANGE = (250., 108., 7.)
PLATE_FRAMES = [53, 54, 69, 110]
KEEP_ROWS_FROM = 380

H_LOGO, H_FINO, H_AMT, G1, G2 = 19.0, 11.0, 44.0, 5.0, 5.0      # misure finali uniformi (0,86 x fase 2)
LOGO_DX = {'goldbet': -1, 'snai': -4, 'netbet': 1}              # logo rispetto al bordo sinistro dell'importo
FINAL_CENTER = {'goldbet': (160, 61.5), 'snai': (160, 190.0), 'netbet': (160, 321.5)}
PHASE2_GEOM = {'goldbet': {'logo': (62, 78, 22), 'fino': (65, 108, 13), 'amt': (64, 128, 51)},
               'netbet': {'logo': (64, 205, 22), 'fino': (66, 235, 13), 'amt': (64, 260, 51)}}
# fasi 1-2: loghi riportati a 22 px e alle proporzioni del file ufficiale (nel master NetBet e' compresso ~11%)
LOGO_FIX = [dict(op='netbet', frames=range(74, 110), old=(64, 205, 171, 226), new=(64, 205, 22)),
            dict(op='goldbet', frames=range(101, 110), old=(62, 76, 175, 99), new=(62, 78, 22))]
REARRANGE = {111: 0.12, 112: 0.24, 113: 0.53, 114: 0.80, 115: 0.92, 116: 1.0}
SNAI_COUNT_FRAMES = range(116, 130)
SNAI_COUNT_ROWS = (108, 275)
SNAI_COUNT_AMT = (159.5, 217.5, 1.617)          # importo del conteggio a f129 (284 px): centro e scala rispetto al riposo nuovo (asset 5.000 v3, 175,7 px)
SNAI_REVEAL = {130: (0.27, 0.22, 0.66), 131: (0.43, 0.43, 0.88), 132: (0.78, 0.73, 1.0), 133: (1.0, 1.0, 1.0)}
GLITCH_NO_SNAI = {134}
REST = (135, 187)
OUTRO = range(188, 211)
OUTRO_THR = 30

# QA
QA_REST = (80, 105, 160)
QA_SHEETS = [((80, 105, 160), '01_riposo_per_fase', 'Riposo: fase 1 NetBet (f80), fase 2 GoldBet+NetBet (f105), finale (f160)'),
             ((143, 145, 147, 149, 150, 151, 152, 154, 156, 158), '02_ex_pulse_SNAI_f145-156', 'Pulse SNAI f145-156 eliminato (sfondo statico: clean plate da frame reali)', (0, 110, 320, 270), 0.8),
             ((109, 110, 111, 112, 113, 114, 115, 116), '03_riordino_pila', 'Riordino f111-116: stessa curva dell\'originale verso le misure uniformi', None, 0.6),
             ((127, 128, 129, 130, 131, 132, 133, 134, 135), '04_conteggio_e_comparsa_SNAI', 'Conteggio SNAI originale (f116-129), comparsa logo/FINO A (f130-133), glitch f134', (0, 110, 320, 270), 0.8),
             ((70, 72, 74, 76, 97, 99, 100, 101, 102), '05_conteggi_e_ingressi', 'Conteggi e ingressi NetBet/GoldBet: pixel originali; logo ufficiale da f74 / f101', None, 0.6),
             ((187, 188, 190, 192, 195, 199, 203, 207, 210), '06_esplosione_chiusura', 'Esplosione di chiusura: simboli originali sopra la composizione corretta', None, 0.6)]
