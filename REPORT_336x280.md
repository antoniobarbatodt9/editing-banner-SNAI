# SNAI Bonus Sport 336×280: render corretto e QA

**Master di riferimento:** `00_master_approvato/SNAI_BonusSport_336x280_MASTER.mp4` (10,0 s, 150 frame, 15 fps).

| Consegna | File |
|---|---|
| Master lossless RGB | `09_rebuild_master/SNAI_BonusSport_336x280_CORRETTO_master_lossless_rgb.mkv` |
| Distribuzione | `11_distribuzione/SNAI_BonusSport_336x280_CORRETTO.mp4`: **692 KB** (originale 734 KB), H.264 High, 336×280, 15 fps, 10,00 s, senza audio, stessi tag colore |
| Confronto affiancato | `10_qa/336x280/confronto_originale_vs_corretto.mp4` |
| Tavole QA | `10_qa/336x280/01…06_*.png`, `TEST_pulse_SNAI_eliminato_f115-127.png`; misure in `qa_report.json` |

Stessa timeline del 300×250 (stessi frame di ingressi, conteggio, uscite e pulse). Stesse regole già approvate:
- misure uniformi;
- conteggio originale ripristinato;
- card SNAI senza pulse;
- CTA con il suo comportamento originale (in questo formato la CTA resta ferma);
- asset della cartella SPORT.

## Struttura del formato

Le tre card compaiono **una alla volta**, nella stessa posizione (card originale 172×149, x 82–253,
y 26–174). Non c'è titolo. **In questo formato le card originali sono opache**: nessuna trasparenza
da gestire. La card SNAI resta a schermo fino all'ultimo frame, senza uscita.

## Misure a riposo (MP4 compresso)

| Operatore | Card | Logo | "FINO A" | Importo |
|---|---|---|---|---|
| William Hill (f60) | 174 × 151 | **25** | **11** | **41** |
| bet365 (f85) | 174 × 151 | **25** | **11** | **41** |
| SNAI (f112) | 174 × 151 | **25** | **11** | **41** |

- **Prima della correzione:** loghi 25/32/32, "FINO A" 11/12/12, importi 43/43/42.
- **Logo a 25 px:** è la misura del logo William Hill originale. SNAI e bet365 scendono da 32 px.
- **Importo a 41 px:** "2.000€" è largo 162 px su una card da 174, con circa 6 px di margine per lato,
  come l'originale (158 px su 172). Stesse proporzioni del 300×250, scalate di 1,12×.

## Conteggio (valori e timing originali)

| Operatore | Sequenza |
|---|---|
| William Hill | f52 20 · 30 · 48 · 66 · 75 · 91 · f58 103 → 105 da f59 |
| bet365 | f74 900 · 865 · 795 · 725 · 655 · 585 · f80 550 → 500 da f81 |
| SNAI | f102 300 · 560 · 820 · 960 · 1.200 · f107 1.450 → 2.000 da f108 |

I valori intermedi sono ritagliati dai fotogrammi originali e portati alla nuova altezza. Il conteggio
finisce prima del pulse (f116).

## Pulse della card SNAI eliminato

- **Tutta la permanenza a schermo ricontrollata** (f108–150): l'unico pulse è il doppio ciclo **f116–126**
  (espansioni f116–119 e f123–126, contrazioni f120–122). Nessun altro ciclo fino alla fine.
- **Contrazioni:** la card resta a misura piena, che copre già l'originale. Nessun pixel ricostruito.
- **⚠ Espansioni (8 frame, 0,53 s): sfondo RICOSTRUITO.** La card ingrandita arrivava quasi al bordo
  alto (y 5) e oltre la parte alta della CTA. La fascia y 0–238 è interpolata con flusso ottico tra i
  frame reali 115→120 e 122→127. **La CTA resta il pixel reale del frame**, sulla sua sagoma esatta, e
  il disclaimer non è toccato. Tavola a luminosità ×4: `TEST_pulse_SNAI_eliminato_f115-127.png`.
- **Verifica sul master:** differenza **0** tra frame consecutivi all'interno delle card a riposo
  (WH f59–66, bet365 f81–89, SNAI f108–150).

## Altre verifiche

- **Fuori dalle card nessun pixel toccato** (esclusi gli 8 frame ricostruiti): differenza massima **0**
  sul master, 1,3 livelli medi sulla distribuzione.
- **Ingressi:** il rettangolo scuro d'ingresso (f51, f73, f100–101) è quello originale; i contenuti
  entrano con la stessa dissolvenza dell'originale (opacità misurata frame per frame).
- **Uscite di WH (f67–69) e bet365 (f90–92):** la card nuova sfuma con l'opacità dell'originale,
  stimata pixel per pixel, senza fantasmi dei vecchi contenuti.
- **Qualità:** PSNR tra distribuzione e master medio 39,8 dB, minimo 35,1 dB.

## Gate

Mi fermo qui finché non arriva un'approvazione esplicita del 336×280.
