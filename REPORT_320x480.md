# SNAI Bonus Sport 320×480: render corretto e QA

**Master di riferimento:** `00_master_approvato/SNAI_BonusSport_320x480_MASTER.mp4`
(7,87 s, 118 frame, 15 fps). La durata è mantenuta.

**Decisioni del cliente applicate:** card opache (A), pulse secondo l'opzione 1, importi a 57 px.

| Consegna | File |
|---|---|
| Master lossless RGB, identico bit per bit al compositing | `09_rebuild_master/SNAI_BonusSport_320x480_CORRETTO_master_lossless_rgb.mkv` |
| Distribuzione | `11_distribuzione/SNAI_BonusSport_320x480_CORRETTO.mp4`: **951 KB** (originale 1,08 MB), H.264 High, 320×480, 15 fps, 7,87 s, senza audio, stessi tag colore |
| Confronto affiancato | `10_qa/320x480/confronto_originale_vs_corretto.mp4` |
| Tavole QA | `10_qa/320x480/01…05_*.png`; misure in `10_qa/320x480/qa_report.json` |
| Test della ricostruzione del pulse, scartata | `10_qa/320x480/TEST_pulse_ricostruzione_f89-99.png` |

## ⚠ Differenza intenzionale: card rese OPACHE

Nell'originale le card sono **semitrasparenti**: attraverso la card si vedono la rete e il pallone
in movimento, circa al 15–20%. Nella versione corretta le card sono **opache**, nel tono della card
originale (fondo 22/22/24, bordo 49/48/52).

**Motivazione:** per togliere i contatori e uniformare logo, "FINO A" e importi bisogna eliminare le
vecchie scritte. Sotto quelle scritte non c'è **nessun dato di sfondo disponibile**: in quei punti,
in quei frame, lo sfondo non compare mai. Mantenere la trasparenza avrebbe richiesto di inventare il
velo di rete sotto il testo. Una card opaca invece copre per intero la card originale, quindi non si
ricostruisce niente.

## Pulse SNAI (opzione 1)

- **Nell'originale (f90–99):** due espansioni (f90–92 fino a 1,27×, f96–98 fino a 1,07×) e due
  contrazioni (f93–95 fino a 0,86×, f99).
- **Contrazioni rimosse:** la card resta a misura piena, che copre già l'originale.
- **Espansioni rimaste, con la stessa ampiezza dell'originale:** lo sfondo sotto la card ingrandita
  non compare in nessun frame. Una card più piccola lo scoprirebbe, e andrebbe inventato. Durante le
  espansioni anche logo e testi si ingrandiscono insieme alla card, restando proporzionati.
- **Ricostruzione dello sfondo scartata:** l'ho testata con flusso ottico tra frame reali. Il risultato
  mostrava un gradino sulla rete nei frame 90 e 96 e, con il bordo sfumato, il contorno fantasma della
  vecchia card (vedi la tavola di test).

## Misure dopo la correzione (MP4 compresso)

Le card compaiono una alla volta, nella stessa posizione (262×228). Misure a riposo:

| Operatore | Card | Logo | "FINO A" | Importo |
|---|---|---|---|---|
| William Hill (f49) | 262 × 228 | **41** | **16** | **57** |
| bet365 (f65) | 262 × 228 | **41** | **16** | **57** |
| SNAI (f85) | 262 × 228 | **41** | **16** | **57** |

- **Prima della correzione:** loghi 38/45/45, "FINO A" 18, importi 63 px.
- **Importi a 57 px:** "2.000€" è largo 226 px e lascia circa 18 px di margine per lato.

## Verifiche

- **Fuori dalle card nessun pixel toccato:** titolo, CTA con il suo pulse, sfondo e disclaimer sono
  identici all'originale (differenza massima **0** sul master, 1,8 livelli medi sulla distribuzione).
- **Importi al valore finale da subito**, con le dissolvenze d'ingresso originali: WH f43,
  bet365 f59–60, SNAI f80. Non ci sono più i conteggi 74→105, 680→500 e 960→2.000.
- **Uscite di WH (f52–53) e bet365 (f68–69, glitch a blocchi):** la card nuova sfuma con l'opacità
  misurata pixel per pixel sull'originale, quindi senza fantasmi dei vecchi importi.
- **Card ferme a riposo:** differenza **0** tra frame consecutivi, anche nei frame 93–95 e 99 dove
  prima c'erano le contrazioni.
- **Qualità:** PSNR tra distribuzione e master medio 39,0 dB, minimo 34,1 dB al f91 (card
  ingrandita).

## Gate

Mi fermo qui finché non arriva un'approvazione esplicita del 320×480.
