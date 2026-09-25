# SNAI Bonus Sport 300×50: render corretto e QA

**Master di riferimento:** `00_master_approvato/SNAI_BonusSport_300x50_MASTER.mp4` (10,0 s, 150 frame, 15 fps).

| Consegna | File |
|---|---|
| Master lossless RGB | `09_rebuild_master/SNAI_BonusSport_300x50_CORRETTO_master_lossless_rgb.mkv` |
| Distribuzione | `11_distribuzione/SNAI_BonusSport_300x50_CORRETTO.mp4`: **127 KB** (originale 141 KB), H.264 High, 300×50, 15 fps, 10,00 s, senza audio, stessi tag colore |
| Confronto (originale sopra, corretto sotto) | `10_qa/300x50/confronto_originale_vs_corretto.mp4` |
| Tavole QA | `10_qa/300x50/01…06_*.png`; misure in `qa_report.json` |

Versione ridotta del 728×90, con la **stessa timeline frame per frame**: ingressi, conteggio, "FINO A"
lettera per lettera, uscite, pulse SNAI f120–127, pulse della CTA f139.

- **Card orizzontale:** originale x 4–178, y 1–35.
- **CTA:** separata a destra (x 204–295) e **invariata**.
- **⚠ Card opache:** come nel 728×90 e nel 320×480, le card originali sono semitrasparenti. Le card
  nuove sono opache, perché sotto le vecchie scritte non c'è alcun dato di sfondo.

## Misure a riposo (MP4 compresso)

| Operatore | Card | Logo | "FINO A" | Importo |
|---|---|---|---|---|
| William Hill (f64) | 177 × 37 | **16** | **5** | **22** |
| bet365 (f86) | 177 × 37 | **16** | **5** | **22** |
| SNAI (f112) | 177 × 37 | **16** | **5** | **22** |

- **Prima della correzione:** loghi 15/17/18, "FINO A" 5/5/4, importi 22.
- **Misure rilevate dal QA:** i loghi risultano 19 px per il bordo antialias. A questa dimensione
  l'antialias pesa di più, ma è uguale per tutti i loghi.
- **Allineamenti:** gli importi sono allineati a destra a x 174 e i loghi di WH e bet365 finiscono a
  x 88. SNAI finisce a x 83, come nell'originale, per lasciare spazio a "2.000€" (87 px).

## Conteggio (valori e timing originali)

| Operatore | Sequenza |
|---|---|
| William Hill | f54 (57, illeggibile: solo il logo in dissolvenza) · 71 · 76 · 86 · 96 · f59 100 → 105 da f60 |
| bet365 | f76 938 · 838 · 741 · 662 · 603 · f81 504 → 500 da f82 |
| SNAI | f100 574 · 813 · 956 · 1.147 · f104 1.386 → 2.000 da f105 |

I valori intermedi sono ritagliati dai fotogrammi originali, ripuliti dal bordo della card e dal rumore.

## Pulse della card SNAI eliminato

- **Ciclo individuato:** l'unico pulse della card SNAI è **f120–127**. Nessun altro ciclo fino alla fine.
- **Contrazioni (f123–124):** la card a misura piena copre già l'originale.
- **⚠ Espansioni (f120–122, f125–127, 0,4 s): sfondo RICOSTRUITO.** La fascia x 0–200, y 0–36 è
  interpolata tra i frame reali 119→123 e 124→128. Il disclaimer resta fuori dal calcolo.
- **Card a riposo:** differenza **0** tra frame consecutivi (WH f63–67, bet365 f85–89, SNAI f108–150).

## Altre verifiche

- **Fuori dalle card:** nessun pixel toccato, esclusi i 6 frame del pulse (differenza massima **0** sul master).
- **Uscite:** WH (f68–71) e bet365 (f90–93) seguono l'opacità dell'originale.
- **Regressione:** 728×90 e 320×480, rigenerati con il codice aggiornato, sono identici bit per bit.

## Gate

Mi fermo qui finché non arriva un'approvazione esplicita del 300×50.
