# SNAI Bonus Casinò 320×480: campione corretto e QA

**Master di riferimento:** `00_master_approvato/casino/SNAI_BonusCasino_320x480_MASTER.mp4` (14,0 s, 210 frame, 15 fps).
**Asset:** cartella `CASINO/` su `main`, copiata in `01_originali_ufficiali/asset_video_CASINO/`.

| Consegna | File |
|---|---|
| Master lossless RGB | `09_rebuild_master/casino/SNAI_BonusCasino_320x480_CORRETTO_master_lossless_rgb.mkv` |
| Distribuzione | `11_distribuzione/casino/SNAI_BonusCasino_320x480_CORRETTO.mp4`: **1,56 MB** (originale 1,66 MB), H.264 High, 320×480, 15 fps, 14,00 s, senza audio, stessi tag colore |
| Confronto affiancato | `10_qa/casino_320x480/confronto_originale_vs_corretto.mp4` |
| Tavole QA | `10_qa/casino_320x480/01…06_*.png`; misure in `qa_report.json` |

## Timeline del master (misurata frame per frame)

| Frame | Contenuto | Trattamento |
|---|---|---|
| f1–52 | sigla BONUS CASINÒ + esplosione di simboli slot | originale |
| f53–68 | conteggio NetBet al centro (1.335 → 2.000) | originale |
| f69, f110 | frame vuoti (glitch dell'originale) | originale |
| f70–82 | NetBet si assesta (fase 1) | originale; logo ufficiale da f74 |
| f83–100 | conteggio GoldBet (1.320 → 2.000) e comparsa | originale |
| f101–109 | fase 2: GoldBet + NetBet | loghi a 22 px, proporzioni ufficiali |
| f111–116 | riordino della pila | ricalcolato con la stessa curva, verso le misure uniformi |
| f116–129 | conteggio SNAI al centro (2.208 → 5.000) | originale |
| f130–133 | comparsa di logo e "FINO A" SNAI (scrittura progressiva) | ricalcolata, stessa curva |
| f134 | glitch originale: SNAI assente per 1 frame | conservato |
| f135–187 | composizione finale a riposo | **pulse SNAI f145–156 eliminato** |
| f162–179 | pulse della CTA | originale, invariato |
| f188–210 | esplosione di chiusura | simboli originali sopra la composizione corretta |

## Sfondo: statico, nessun pixel inventato

I frame vuoti (f53, f54, f69, f110) coincidono entro **3 livelli**. Il clean plate è la loro mediana:
sono pixel reali. Nel rimpicciolire SNAI e togliere il pulse, lo sfondo scoperto viene da lì.

## Misure a riposo (MP4 compresso)

**Composizione finale (f160), misura unica nuova:**

| Operatore | Logo | "FINO A" | Importo |
|---|---|---|---|
| GoldBet | **19** | **11** | **44** (45 con antialias) |
| SNAI | **19** | **11** | **44** |
| NetBet | **19** | **11** | **44** (45 con antialias) |

Prima della correzione: GoldBet 18 / 10 / 37, SNAI 25 / 16 / 55, NetBet 15 / 11 / 36.

- **Fasi 1–2 (f80, f105):** logo 22, "FINO A" 13, importo 51 per entrambi gli operatori. La misura
  finale è proporzionale a queste (0,86×). Prima della correzione i loghi erano NetBet 22 e GoldBet 24.
- **Posizioni:** i blocchi restano centrati sugli stessi assi verticali dell'originale (y 61 / 190 / 321).
- **⚠ Logo NetBet deformato nel master:** nel video il logo NetBet è compresso in orizzontale di circa
  l'11% (108×22 invece di 121×22 del file ufficiale). Nel corretto uso le **proporzioni ufficiali** in
  tutte le fasi. GoldBet e SNAI coincidono già con i file ufficiali entro il 2%.
- **Colori:** bianco (254,254,255) e arancio (250,108,7) campionati dal master.

## Pulse

- **Scansione di tutta la finestra di riposo (f135–187):** la card SNAI ha **un solo ciclo, doppio**,
  a f145–156 (espansione f145–149, rientro, di nuovo f151–152, rientro fino a f156). L'ho eliminato:
  nel master la differenza tra frame consecutivi è **0**, contro 212 nell'originale.
- **GoldBet e NetBet:** nessun pulse in nessuna fase.
- **CTA:** il pulse (f162–179) resta invariato.

## Verifiche

- **CTA e disclaimer** (righe ≥ 380): identici all'originale in tutti i 210 frame (differenza 0 sul master).
- **Frame non toccati** (sigla, conteggi NetBet/GoldBet, glitch): identici all'originale.
- **Conteggi:** tutti e tre sono pixel originali. Nei frame del conteggio SNAI (f116–129) vengono
  ridisegnati solo GoldBet e NetBet.
- **Esplosione di chiusura:** i simboli sono isolati per differenza dal frame di riposo e restano
  originali; tra un simbolo e l'altro si vede la composizione corretta.

## Gate

Campione per la linea Casinò: mi fermo qui finché non arriva un'approvazione esplicita, prima di
propagare agli altri formati.
