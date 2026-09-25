# SNAI Bonus Sport 320×320: render corretto e QA

**Master di riferimento:** `00_master_approvato/SNAI_BonusSport_320x320_MASTER.mp4` (10,0 s, 150 frame, 15 fps).

| Consegna | File |
|---|---|
| Master lossless RGB | `09_rebuild_master/SNAI_BonusSport_320x320_CORRETTO_master_lossless_rgb.mkv` |
| Distribuzione | `11_distribuzione/SNAI_BonusSport_320x320_CORRETTO.mp4`: **765 KB** (originale 809 KB), H.264 High, 320×320, 15 fps, 10,00 s, senza audio, stessi tag colore |
| Confronto affiancato | `10_qa/320x320/confronto_originale_vs_corretto.mp4` |
| Tavole QA | `10_qa/320x320/01…07_*.png`, `TEST_pulse_SNAI_eliminato_f115-128.png`; misure in `qa_report.json` |

Stesse regole approvate per 300×250 e 336×280. Le tre card compaiono **una alla volta**, nella stessa
posizione (card originale 172×149, x 74–245, y 42–190). Le card originali sono **opache** e non c'è titolo.
La timeline è propria di questo formato, misurata frame per frame.

## ⚠ Errore nel master originale corretto: card NetBet al f92

Nel master originale, al **frame 92** (t = 6,07 s), la card bet365 in dissolvenza viene sostituita
per un fotogramma da una card **NetBet** con importo, un brand che non fa parte di questa campagna.
Nel corretto il riquadro della card al f92 usa i **pixel reali del frame 93**: in quel punto la card
bet365 è già svanita al f91 e il f93 non ha card. Tavola: `07_f92_netbet_rimosso.png`.

## Misure a riposo (MP4 compresso)

| Operatore | Card | Logo | "FINO A" | Importo |
|---|---|---|---|---|
| William Hill (f64) | 174 × 151 | **25** | **11** | **41** |
| bet365 (f86) | 174 × 151 | **25** | **11** | **41** |
| SNAI (f112) | 174 × 151 | **25** | **11** | **41** (42 con antialias) |

- **Prima della correzione:** loghi 24/32/30, "FINO A" 12, importi 42/42/40.
- **Proporzioni:** le misure sono identiche al 336×280, perché la card originale ha la stessa dimensione.
  "2.000€" è largo circa 162 px su una card da 174.

## Conteggio (valori e timing originali)

| Operatore | Sequenza |
|---|---|
| William Hill | f54 32 · 75 · 84 · 100 · 103 · f59 104 → 105 da f60 |
| bet365 | f76 760 · 695 · 625 · 570 · 550 · f81 515 → 500 da f82 |
| SNAI | f104 925 · 1.050 · 1.200 · 1.400 · f108 1.450 → 2.000 da f109 |

I valori intermedi sono ritagliati dai fotogrammi originali e portati alla nuova altezza. Nei frame
in dissolvenza (bassa opacità) il ritaglio è ripulito dallo sfondo che traspare. Il conteggio finisce
prima del pulse (f116).

## Pulse della card SNAI eliminato

- **Tutta la permanenza a schermo ricontrollata** (f109–150): l'unico pulse è **f116–127**
  (espansioni f116–120 e f124–127, contrazioni f121–122).
- **Contrazioni:** la card a misura piena copre già l'originale.
- **⚠ Espansioni (9 frame, 0,6 s): sfondo RICOSTRUITO.** La fascia y 0–218 è interpolata con flusso
  ottico tra i frame reali 115→121 e 123→128. La CTA resta sempre il pixel reale.
- **Pulse della CTA:** in questo formato la CTA ha un proprio pulse (f137–144), che resta **invariato**.
- **Verifica sul master:** differenza **0** tra frame consecutivi all'interno delle card a riposo
  (WH f60–67, bet365 f82–87, SNAI f109–150).

## Altre verifiche

- **Fuori dalle card nessun pixel toccato** (esclusi i 9 frame del pulse e il f92): differenza massima
  **0** sul master, 1,4 livelli medi sulla distribuzione.
- **Uscite:** WH (f68–70) e bet365 (f88–91) sfumano con l'opacità misurata sull'originale.
- **Regressione:** il 300×250, rigenerato con il codice aggiornato, è identico bit per bit.

## Gate

Mi fermo qui finché non arriva un'approvazione esplicita del 320×320.
