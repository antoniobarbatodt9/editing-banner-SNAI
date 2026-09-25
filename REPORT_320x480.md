# SNAI Bonus Sport 320×480: render corretto e QA (v5)

**Master di riferimento:** `00_master_approvato/SNAI_BonusSport_320x480_MASTER.mp4`
(7,87 s, 118 frame, 15 fps). La durata è mantenuta.

**Decisioni del cliente applicate:** card opache (A), card SNAI senza pulse (v5), CTA con il suo pulse, importi a 57 px, conteggio ripristinato (v4).

| Consegna | File |
|---|---|
| Master lossless RGB, identico bit per bit al compositing | `09_rebuild_master/SNAI_BonusSport_320x480_CORRETTO_master_lossless_rgb.mkv` |
| Distribuzione | `11_distribuzione/SNAI_BonusSport_320x480_CORRETTO.mp4`: **951 KB** (originale 1,08 MB), H.264 High, 320×480, 15 fps, 7,87 s, senza audio, stessi tag colore |
| Confronto affiancato | `10_qa/320x480/confronto_originale_vs_corretto.mp4` |
| Tavole QA | `10_qa/320x480/01…05_*.png`; misure in `10_qa/320x480/qa_report.json` |
| Test della ricostruzione del pulse, scartata | `10_qa/320x480/TEST_pulse_ricostruzione_f89-99.png` |

## Conteggio degli importi ripristinato (v4)

Il conteggio progressivo dell'originale era stato tolto per errore. L'istruzione di togliere le oscillazioni
riguardava solo il rimbalzo di scala (il pulse), non il conteggio. Ora è ripristinato con **gli stessi valori
e lo stesso timing dell'originale**, fotogramma per fotogramma, alla nuova dimensione uniforme delle cifre.
Il conteggio finisce sempre **prima** che parta il pulse.

| Operatore | Sequenza originale (un valore per frame) |
|---|---|
| William Hill | f43 74 · f44 86 · f45 100 · f46 104 → 105 da f47 |
| bet365 | f60 680 · f61 570 · f62 530 → 500 da f63; a f59, dove la cifra originale non si legge, uso 680 |
| SNAI | f80 960 · f81 1.210 · f82 1.410 · f83 1.470 → 2.000 da f84 (pulse da f89/90) |

- **Font:** gli asset forniti contengono solo 0, 1, 2, 5, il punto e €; le cifre 3, 4, 6, 7, 8 e 9 non ci
  sono. Ogni valore intermedio è quindi **ritagliato dal fotogramma originale** in cui compare (stesso font
  e stessa spaziatura del video), portato all'altezza uniforme nuova (sempre in riduzione o a parità, mai
  ingrandito) e centrato sulla posizione del valore finale, come nell'originale. "FINO A" resta fermo.
  Nei frame in dissolvenza la posizione del numero è presa dal frame leggibile vicino.
- **Differenza di stile nel passaggio al valore finale:** il valore finale è l'asset pulito fornito, un
  po' più grassetto e più inclinato del font del video. Nel passaggio dall'ultimo valore intermedio al
  finale la differenza è percepibile. Se fornite le cifre 0–9 nello stile dell'asset pulito, ricompongo i
  valori intermedi con quelle.
- **Tutto il resto invariato:** fuori dai frame del conteggio il master è identico bit per bit alla
  versione già consegnata (verificato frame per frame).
- **Tavola:** `06_conteggio_ripristinato.png`, originale sopra, MP4 corretto sotto.

## ⚠ Differenza intenzionale: card rese OPACHE

Nell'originale le card sono **semitrasparenti**: attraverso la card si vedono la rete e il pallone
in movimento, circa al 15–20%. Nella versione corretta le card sono **opache**, nel tono della card
originale (fondo 22/22/24, bordo 49/48/52).

**Motivazione:** per uniformare logo, "FINO A" e importi bisogna eliminare le
vecchie scritte. Sotto quelle scritte non c'è **nessun dato di sfondo disponibile**: in quei punti,
in quei frame, lo sfondo non compare mai. Mantenere la trasparenza avrebbe richiesto di inventare il
velo di rete sotto il testo. Una card opaca invece copre per intero la card originale, quindi non si
ricostruisce niente.

## Pulse SNAI eliminato (v5)

Su richiesta del cliente la card SNAI **non pulsa mai**: dal termine del conteggio (f84) all'uscita (f116)
resta ferma a misura di riposo. Verifica sul master: differenza **0** tra fotogrammi consecutivi
all'interno della card in tutta la finestra f84–115.

- **Tutta la permanenza a schermo ricontrollata** (f84–115), misurando il bordo della card originale
  frame per frame. L'unico pulse della card SNAI è il doppio ciclo **f90–99** (espansione f90–92,
  contrazione f93–95, espansione f96–98, contrazione f99).
- **f112–114:** a ingrandirsi è la **CTA "SCOPRI DI PIÙ"** (fino a +22%), il cui pulse resta invariato
  come da brief. Il bordo della card SNAI in quei frame è fermo a misura di riposo sia nell'originale
  sia nel corretto.
- **Contrazioni (f93–95, f99):** card a misura piena, che copre già l'originale. Nessun pixel ricostruito.
- **⚠ Espansioni (f90–92, f96–98): sfondo RICOSTRUITO.** Con la card a misura di riposo si scoprirebbe
  sfondo che nell'originale non compare in nessun frame. In quei 6 fotogrammi (0,4 s) la fascia tra
  titolo e CTA è interpolata con flusso ottico tra i fotogrammi reali più vicini (89→93 e 95→99), su
  tutta la larghezza e con bordo sfumato di 8 px, così non si vede il gradino del primo test. Titolo,
  CTA con il suo pulse e disclaimer restano i pixel reali del frame. Sono stati tolti i residui arancio
  trascinati dal flusso ottico, verificato a luminosità ×4. Tavola:
  `TEST_v5_pulse_SNAI_eliminato_f89-99.png`.
- Rispetto alla v4 cambiano **solo** i fotogrammi 90, 91, 92, 96, 97 e 98; il resto è identico bit per bit.

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
- **Importi:** conteggio originale ripristinato (v4: 74→105, 680→500, 960→2.000), con le
  dissolvenze d'ingresso originali (WH f43, bet365 f59–60, SNAI f80).
- **Uscite di WH (f52–53) e bet365 (f68–69, glitch a blocchi):** la card nuova sfuma con l'opacità
  misurata pixel per pixel sull'originale, quindi senza fantasmi dei vecchi importi.
- **Card ferme a riposo:** differenza **0** tra frame consecutivi, dal termine del conteggio all'uscita
  (WH f47–51, bet365 f63–67, SNAI f84–115).
- **Qualità:** PSNR tra distribuzione e master medio 39,0 dB, minimo 34,1 dB al f91 (card
  ingrandita).

## Gate

Mi fermo qui finché non arriva un'approvazione esplicita del 320×480.
