# SNAI Bonus Sport 300×600: render campione corretto e QA (v3)

**Modifica della v3:** l'importo 2.000€ è ora il nuovo asset, più pulito, caricato su `main` (commit `bd57228`, `SPORT/…/text_2000.png`). Resta alto 39 px e diventa largo 154 px, con 10 px di margine per lato nella card. Il resto è invariato rispetto alla v2.


**Modifiche della v2, su tua richiesta:**
- Loghi, "FINO A" e importi presi dagli asset estratti dal video (cartella `SPORT/` su `main`,
  copiata in `01_originali_ufficiali/asset_video_SPORT/`). Gli importi sono di nuovo nel **font
  originale** e il font sostitutivo Saira è stato rimosso.
- Card SNAI: logo **4 px più su**; "FINO A" e 2.000 € **4 px più giù**. "FINO A" si sposta insieme alla
  cifra per restare agganciato all'importo.


**Master di riferimento:** `00_master_approvato/SNAI_BonusSport_300x600_MASTER_2000.mp4`
(importo SNAI 2.000 €; sha256 `9d7dff8c…d8e06c`). Il file 1.500 € è archiviato come superato.

| Consegna | File |
|---|---|
| Master ad alta qualità, lossless RGB, identico bit per bit ai PNG del compositing | `09_rebuild_master/SNAI_BonusSport_300x600_CORRETTO_master_lossless_rgb.mkv` (9,9 MB) |
| Versione di distribuzione | `11_distribuzione/SNAI_BonusSport_300x600_CORRETTO.mp4`: **922 KB** (originale 949 KB), H.264 High, 300×600, 15 fps, 135 frame, 9,00 s, senza audio, stessi tag colore dell'originale (yuvj420p full range, BT.709) |
| Confronto affiancato originale / corretto | `10_qa/confronto_originale_vs_corretto.mp4` |
| Tavole QA dei frame critici | `10_qa/01…05_*.png`; valori misurati in `10_qa/qa_report.json` |

Tutte le misure qui sotto sono prese sul **file MP4 compresso finale**, decodificato.

---

## 1. Principio adottato: nessuna modifica al video originale fuori dalle card

- Fuori dalle card nuove ogni pixel è quello originale: sfondo, titolo, CTA con il suo pulse, disclaimer 18+/ADM.
  Verifica sul master: differenza massima **0** su tutti i 135 frame. Sulla distribuzione lo scarto medio
  è di 1,2 livelli, dovuto solo alla compressione.
- Ogni card nuova copre sempre per intero la card originale dello stesso frame, con almeno 1 px di margine.
  Così non viene mai scoperto né ricostruito sfondo che nell'originale era nascosto. Per questo la card
  SNAI mantiene l'ingombro originale (vedi punto 5).
- Unico intervento sullo sfondo, indispensabile per togliere il pulse SNAI (f82–85 e f89–92): l'anello
  che la card ingrandita copriva viene riempito con i pixel originali degli stessi punti ai frame 81 e 93.
  Lì lo sfondo è nero e statico (è in lenta dissolvenza), quindi i pixel vengono interpolati tra i due
  frame. Non c'è nulla di generato.
- Ordine di ingresso, tempi, CTA, titolo, palette e disclaimer sono invariati.

## 2. Misure dopo la correzione (MP4 compresso)

Le altezze sono l'ingombro dell'inchiostro in px, bordi antialias inclusi dal 30% di copertura.

**Tre card (frame 100, t = 6,60 s):**

| Operatore | Card (L×A) | Logo | "FINO A" | Importo | Logo L/A reso / ufficiale |
|---|---|---|---|---|---|
| bet365 | 174 × 131 | **21** | **10** | **39** | 90×21 = 4,29 / 4,25 |
| SNAI | 174 × **154** | **21** | **10** | **39** | 93×21 = 4,43 / 4,43 |
| William Hill | 174 × 131 | **21** | **10** | **39** | 102×21 = 4,86 / 4,84 |

Prima della correzione: loghi 22/29/20, "FINO A" 11/14/10, importi 40/40/38, card larghe 124/169/126 px.

- Spazio tra le card: **6 px** e **6 px**, uniforme (prima 11 e 21 px).
- Il gruppo è centrato: 13 px tra titolo e prima card, 13 px tra ultima card e CTA.

**Fasi precedenti, con le card grandi originali:** WH da solo (f47) e bet365+WH (f60). Card 174×152,
logo **28**, "FINO A" **13**, importo **51** per entrambi gli operatori (prima i loghi erano 31 e 25 px).
Sono le stesse proporzioni della fase a tre card, scalate di 1,31×.

## 3. Rimbalzi e pulse rimossi

| Elemento | Prima | Dopo |
|---|---|---|
| Importo WH (f43–46) | conta 68 → 80 → … → 105 | 105 € fin dal primo frame visibile |
| Importo bet365 (f52–54) | parte da 900, poi 878, 648, fino a 500 | 500 €, con la stessa dissolvenza d'ingresso |
| Importo SNAI (f66–76) | conta 300 → 546 → 784 → … → 2.000 | 2.000 €, con la stessa dissolvenza d'ingresso |
| Card SNAI (f82–92) | pulse 1,27× → 0,85× → 1,1× → 1,0 | ferma |
| Card, loghi e testi dopo l'ingresso | — | identici da un frame all'altro: sul master la differenza massima tra frame consecutivi è **0** per tutte le card |
| CTA "SCOPRI DI PIÙ" | pulse | **invariato**: sono i pixel originali |

Riferimento: nell'originale, durante il pulse, lo stesso riquadro SNAI varia in media di 41,5 livelli tra un frame e il successivo.

## 4. Report QA sui frame critici

- **`02_ex_pulse_SNAI_f80-93.png`**, prima, durante e dopo il vecchio pulse (f80, 82, 83, 84, 86, 87, 89,
  91, 93): card SNAI ferma. L'anello riempito non mostra bordi né cuciture anche con la luminosità
  aumentata di 4 volte (controllo fatto a 4×).
- **`03_ingressi_senza_contatori.png`**: gli importi compaiono subito al valore finale; le dissolvenze
  d'ingresso originali sono conservate (bet365 f52–53, SNAI f66–67).
- **`04_transizione_fase2_fase3.png`** (f62–70): le card si restringono e si spostano in modo monotono
  (senza rimbalzo) e coprono sempre quelle originali. Controllo automatico: nessun pixel di card
  originale visibile fuori dalle nuove nei frame 43–64. Dal f70 lo sfondo nero ha lo stesso colore delle
  card e il test automatico non è applicabile, quindi ho controllato quei frame a vista.
- **`05_uscita.png`** (f122–127): nel master le card sfumano verso il nero con opacità 0,95 / 0,52 / 0,26.
  Le card nuove seguono la stessa curva, senza fantasmi dei contenuti vecchi.
- **Qualità della compressione:** PSNR distribuzione contro master medio 41,8 dB, minimo 36,9 dB al f34
  (flash dell'intro, fuori dalle card).

## 5. Punti da approvare

1. **Card SNAI più alta delle altre (154 contro 131 px).** Con altezze uguali andrebbe scoperto sfondo
   che nell'originale è sempre coperto dalla card SNAI (rete e pallone in movimento, poi la texture
   finale), e andrebbe inventato. Hai escluso qualunque modifica del video originale, quindi la SNAI
   conserva il suo ingombro. Larghezze, loghi, "FINO A" e importi sono invece uniformi, e il contenuto
   della SNAI è centrato nella sua card.
2. **Font degli importi:** risolto nella v2. Gli importi sono gli asset originali del video, ridimensionati in proporzione e ricolorati con il bianco e l'arancio campionati dal master.
3. **Scala delle fasi 1–2** (WH da solo, bet365+WH): ho applicato le stesse proporzioni della fase a
   tre card (28/13/51 px) mantenendo le card grandi originali. Se vuoi 21/10/39 anche lì, le card
   andrebbero rimpicciolite sopra il pallone in movimento, con lo stesso problema di sfondo scoperto del
   punto 1.
4. **Colori.** Loghi e testi sono resi nello spazio colore del master: il bianco dei testi è campionato
   a 234, l'arancio dell'importo SNAI a 254/109/9, come nell'originale. La palette resta invariata.

## 6. Asset usati

- Loghi, "FINO A" e importi: gli asset forniti (`01_originali_ufficiali/asset_video_SPORT/`). Nulla è
  rigenerato; le scale sono uniformi, quindi niente deformazioni.
- Card: ricostruite in modo deterministico con le misure dell'originale (raggio 11 px, fondo 19/20/24,
  bordo 47/48/52).
- Tutto è riproducibile:
  1. `python3 scripts/compose.py FRAMES_ORIGINALI OUT layout.json`
  2. `scripts/encode.sh OUT`
  3. `python3 scripts/qa.py …` e `python3 scripts/qa_sheets.py …`
- Rigenerazione completa (render, encode, QA): circa 70 secondi.
- Timeline frame per frame: `02_inventory/timeline_corretta_e_layout.json`.

## Gate

Mi fermo qui, con render campione e report QA consegnati. Non propago la correzione ad altri formati
finché non arriva un'approvazione esplicita, in particolare sui punti 1 e 3.
