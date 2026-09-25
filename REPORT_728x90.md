# SNAI Bonus Sport 728×90: render corretto e QA

**Master di riferimento:** `00_master_approvato/SNAI_BonusSport_728x90_MASTER.mp4` (10,0 s, 150 frame, 15 fps).

| Consegna | File |
|---|---|
| Master lossless RGB | `09_rebuild_master/SNAI_BonusSport_728x90_CORRETTO_master_lossless_rgb.mkv` |
| Distribuzione | `11_distribuzione/SNAI_BonusSport_728x90_CORRETTO.mp4`: **411 KB** (originale 438 KB), H.264 High, 728×90, 15 fps, 10,00 s, senza audio, stessi tag colore |
| Confronto (originale sopra, corretto sotto) | `10_qa/728x90/confronto_originale_vs_corretto.mp4` |
| Tavole QA | `10_qa/728x90/01…06_*.png`; misure in `qa_report.json` |

## Struttura del formato orizzontale

- **Card orizzontale:** compare una alla volta nella stessa posizione (originale x 75–418, y 4–69).
- **Impaginazione della card:** logo a sinistra, "FINO A" sopra la fine del logo, importo allineato a destra.
- **CTA:** è separata a destra (x 470–655) e ha un proprio pulse (f139), che resta invariato.
- **"FINO A" lettera per lettera:** nell'originale compare scritto progressivamente subito dopo il
  conteggio (WH f60–63, bet365 f81–85, SNAI f105–108). Ho conservato l'animazione con lo stesso
  timing.
- **⚠ Card opache:** come nel 320×480 approvato, le card originali sono semitrasparenti (si vede la
  rete). Le card nuove sono opache, perché sotto le vecchie scritte non c'è alcun dato di sfondo.

## Misure a riposo (MP4 compresso)

| Operatore | Card | Logo | "FINO A" | Importo |
|---|---|---|---|---|
| William Hill (f64) | 346 × 68 | **27** | **11** | **42** |
| bet365 (f86) | 346 × 68 | **27** | **11** | **42** |
| SNAI (f112) | 346 × 68 | **27** | **11** | **42** |

- **Prima della correzione:** loghi 28/31/30, "FINO A" 12/12/11, importi 44.
- **Allineamenti:** tutti i loghi finiscono a x 241 e tutti gli importi a x 412, sulla stessa linea di base.
- **Nota sulla misura SNAI:** lo script QA rileva "FINO A" 12 e importo 44 perché le rispettive zone
  di misura si toccano (il "2" è vicino a "FINO A"). Le altezze impostate sono le stesse per tutti.

## Conteggio (valori e timing originali)

| Operatore | Sequenza |
|---|---|
| William Hill | f54 (57, illeggibile anche nell'originale: solo il logo in dissolvenza) · 71 · 76 · 86 · 96 · f59 100 → 105 da f60 |
| bet365 | f76 938 · 838 · 741 · 662 · 603 · f81 504 → 500 da f82 |
| SNAI | f99 334 · 574 · 813 · 956 · 1.147 · f104 1.386 → 2.000 da f105 |

## Pulse della card SNAI eliminato

- **Ciclo individuato:** l'unico pulse della card SNAI è **f120–127** (espansioni f120–122 e f125–127,
  contrazioni f123–124). Nessun altro ciclo fino alla fine.
- **⚠ Espansioni (6 frame, 0,4 s): sfondo RICOSTRUITO.** La fascia a sinistra della CTA (x 0–445,
  y 0–72) è interpolata con flusso ottico tra i frame reali 119→123 e 124→128.
- **Accorgimenti sulla ricostruzione:** il disclaimer resta fuori dal calcolo, e ho tolto i residui
  chiari e arancio trascinati dal flusso. Verificato a luminosità ×3.
- **Card a riposo:** differenza **0** tra frame consecutivi (WH f63–67, bet365 f85–89, SNAI f108–150).

## Altre verifiche

- **Fuori dalle card nessun pixel toccato** (esclusi i 6 frame del pulse): differenza massima **0** sul
  master, 1,6 livelli medi sulla distribuzione.
- **Uscite:** WH (f68–71) e bet365 (f90–93) seguono l'opacità dell'originale, stimata pixel per pixel.
- **Regressione:** 320×320 rigenerato con il codice aggiornato, identico bit per bit.

## Gate

Mi fermo qui finché non arriva un'approvazione esplicita del 728×90.
