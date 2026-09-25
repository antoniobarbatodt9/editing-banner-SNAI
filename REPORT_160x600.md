# SNAI Bonus Sport 160×600: render corretto e QA

Declinazione del 300×600 approvato (v3), con le stesse regole, gli stessi asset e gli stessi ritocchi.

**Master di riferimento:** `00_master_approvato/SNAI_BonusSport_160x600_MASTER.mp4` (sha256 `97362367…`).

| Consegna | File |
|---|---|
| Master lossless RGB, identico bit per bit al compositing | `09_rebuild_master/SNAI_BonusSport_160x600_CORRETTO_master_lossless_rgb.mkv` |
| Distribuzione | `11_distribuzione/SNAI_BonusSport_160x600_CORRETTO.mp4`: **550 KB** (originale 580 KB), H.264 High, 160×600, 15 fps, 9,00 s, senza audio, stessi tag colore |
| Confronto affiancato originale / corretto | `10_qa/160x600/confronto_originale_vs_corretto.mp4` |
| Tavole QA | `10_qa/160x600/01…05_*.png`; misure in `10_qa/160x600/qa_report.json` |

## Differenze di timeline rispetto al 300×600

Le ho misurate su questo master:
- WH entra a f51–53.
- bet365 entra a f72–74.
- La transizione verso le tre card avviene a f98–99, l'ingresso SNAI a f98–100.
- Il pulse SNAI è a **f116–126**: la card esce anche dal bordo del banner.
- **Non c'è uscita**: le card restano a schermo fino all'ultimo frame.

## Misure dopo la correzione (MP4 compresso)

Le altezze sono l'ingombro dell'inchiostro in px, bordi antialias inclusi dal 30% di copertura.

**Tre card (f110):**

| Operatore | Card (L×A) | Logo | "FINO A" | Importo |
|---|---|---|---|---|
| bet365 | 151 × 118 | **20** | **9** | **34** |
| SNAI | 151 × **133** | **20** | **9** | **34** |
| William Hill | 151 × 118 | **20** | **9** | **34** |

- **Prima della correzione:** loghi 20/24/16, "FINO A" 9/13/9, importi 34/34/35; card larghe 110/149/108.
- **Target:** come nel 300×600, bet365 resta quasi invariato, SNAI si riduce e WH si ingrandisce.
  L'importo SNAI a 34 px è largo 135 px ed entra nella card da 151 px.
- **Spaziatura:** 4 px tra le card, uniforme. È il massimo possibile senza scoprire sfondo nascosto
  (vedi il punto aperto sotto).
- **Titolo e CTA:** 11 px tra il titolo e la prima card, circa 7 px tra l'ultima card e la CTA.
- **SNAI:** logo 3 px più su, "FINO A" e 2.000€ 3 px più giù, come nel 300×600 approvato
  (lì erano 4 px, proporzionati alla card).

**Fasi 1–2 (f60, f85):** card 151×138. Logo **26**, "FINO A" **12** e importo **44** per bet365 e WH
(prima i loghi erano 27 e 22 px).

## Verifiche

- **Sfondo, titolo, CTA e disclaimer invariati:** differenza massima **0** sul master, 1,7 livelli
  medi sulla distribuzione (solo compressione).
- **Card coperte:** le card nuove coprono sempre le originali. Il controllo automatico sui frame
  52–99 non trova residui: le poche righe segnalate sono il bordo antialias della card nuova, dove
  l'originale è già sfondo. Dal f100 lo sfondo nero ha lo stesso colore delle card e i frame sono
  stati controllati a vista.
- **Pulse SNAI rimosso:** la zona coperta dalla card ingrandita è riempita con i pixel originali dei
  frame di riposo 115 e 127 (sfondo nero statico). Non ci sono cuciture, verificato con luminosità ×6.
- **Importi:** compaiono subito al valore finale, con le stesse dissolvenze d'ingresso dell'originale.
- **Card ferme:** differenza massima 0 tra frame consecutivi dopo l'ingresso, per tutte le card.
- **Regressione:** il 300×600 rigenerato con il nuovo codice parametrico risulta identico bit per bit
  a quello consegnato.

## Punto aperto (come nel 300×600)

La card SNAI conserva l'ingombro originale (151×133), perché accorciarla scoprirebbe sfondo che
nell'originale è sempre coperto. Per lo stesso motivo lo spazio tra le card è di 4 px: gli spazi
possono cadere solo dove nell'originale lo sfondo era già visibile.

## Gate

Mi fermo qui finché non arriva un'approvazione esplicita del 160×600.
