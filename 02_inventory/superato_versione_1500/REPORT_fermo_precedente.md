# SNAI Bonus Sport 300×600 — Diagnosi e arresto

**Esito: FERMO. Condizione di arresto n. 1 verificata.** Lo sfondo dietro alla card SNAI
non è statico, e la parte che resterebbe scoperta non è mai visibile in nessun fotogramma.
Non è quindi possibile isolarla senza inventarla. Per questo **non ho prodotto il render
campione**: servirebbe una toppa inventata, che il brief vieta.

Sorgente: `00_master_approvato/SNAI_BonusSport_300x600_originale.mp4`
(sha256 `b96fcfee…a5aa98`, H.264 High, 300×600, 15 fps, 135 frame, 9,0 s, 1181 kb/s, senza audio).
Misure complete in `02_inventory/misure_e_timeline.json`. Coordinate in px sul canvas 300×600,
frame numerati da 1.

---

## 1. Misure attuali al riposo (frame 100, t = 6,60 s)

| Operatore | Card (L×A) | Logo (A) | "FINO A" (A) | Importo (A) |
|---|---|---|---|---|
| bet365 | 124 × 119 | 22 | 11 | 40 |
| SNAI | **169 × 149** | **29** | **14** | 40 |
| William Hill | 126 × 107 | 20 | 10 | 38 |

Spaziatura tra le card: bet365→SNAI 11 px, SNAI→WH 21 px (non uniforme).
Titolo: y 20–57. CTA: y 512–541.

Nelle fasi precedenti le card sono più grandi (~165×148) e le misure non sono uniformi
neanche lì. Al frame 60, per esempio, il logo bet365 è alto 31 px e quello WH 25 px.

## 2. Misure target proposte (fase a tre card)

Le misure sono pianificate ma non ancora applicate, per il motivo spiegato al punto 3.

| Operatore | Card (L×A) | Box card | Logo | "FINO A" | Importo | Scala logo |
|---|---|---|---|---|---|---|
| bet365 | 169 × 118 | 66,92 → 234,209 | 21 | 10 | 39 | 0,955 |
| SNAI | 169 × 118 | 66,226 → 234,343 | 21 | 10 | 39 | 0,724 |
| William Hill | 169 × 118 | 66,360 → 234,477 | 21 | 10 | 39 | 1,05 |

- Larghezza comune 169 px. È la larghezza minima utile: "1.500€" alto 39 px è largo circa
  141 px e non entra nelle card larghe 124–126.
- Spaziatura uniforme di 16 px. Il gruppo è centrato a y 284,5, cioè al centro dello spazio
  tra titolo e CTA.
- A queste misure nessun elemento diventa illeggibile. Il logo WH va ingrandito del 5%, una
  perdita di nitidezza trascurabile a dimensione reale. Resta però un ritaglio dal video, non
  un asset ufficiale.

## 3. Verifica dello sfondo dietro alle card (motivo del fermo)

| Frame | Tempo | Sfondo dietro/attorno alle card | Statico? |
|---|---|---|---|
| 42–72 | 2,73–4,73 s | Pallone e rete in zoom, texture chiara in movimento (luminanza fino a 250). La rete bianca arriva al bordo inferiore e sinistro della card SNAI. | **No** |
| 73–112 | 4,80–7,40 s | Fondo quasi nero con grana, in lenta dissolvenza (luminanza media da ~15 a ~1,5). | Quasi (ricostruibile) |
| 113–126 | 7,47–8,33 s | Una tendina con texture grigio-verde entra da sinistra e passa dietro le card: dal frame 120 compare anche negli spazi tra le card (picchi 46–48). | **No** |

**Perché non si può isolare.** Con card SNAI della stessa misura delle altre, due strisce
della vecchia card restano scoperte: y 210–225 e y 344–358, larghe 169 px, dal frame 65 al
frame 126. In ogni fotogramma in cui la SNAI è presente, quel tratto di sfondo è coperto
dalla card opaca. Prima dell'ingresso della SNAI lo sfondo mostrava un'altra inquadratura
(zoom sul pallone). Non esiste quindi un tratto di sfondo pulito da cui ricavarlo.

Nei frame 66–72 e 113–126 le strisce andrebbero riempite con rete e texture inventate. Il
risultato sarebbe una toppa visibile in movimento.

Ho verificato anche un layout alternativo che evita di scoprire sfondo. Perché la vecchia
card SNAI resti sempre coperta, gli spazi tra le card devono cadere nelle bande di sfondo già
visibili (y 199–209 e 359–379). Questo impone alla SNAI un'altezza di almeno 149 px. Con tre
card uguali di 149 px il gruppo non entra tra titolo e CTA. È quindi incompatibile con
"card SNAI della stessa dimensione delle altre".

Prove visive:
- `10_qa/evidenza_sfondo_strisce_da_rivelare.png`: luminosità ×4. In rosso le strisce da
  scoprire, in ciano le card target.
- `10_qa/pulse_SNAI_f80-94.png`: la sequenza del pulse.
- `02_inventory/frames_riposo/`: i tre fotogrammi di riposo (WH solo, bet365+WH, tre card).

## 4. Rimbalzi e pulse trovati

| Elemento | Frame | Comportamento attuale |
|---|---|---|
| Importo WH | 43–46 | Conta 68 → 92 → 100 → 105 |
| Importo bet365 | 52–55 | Parte da 900 e scende: 900 → 760 → 648 → 500 |
| Importo SNAI | 65–76 | Conta 300 → … → 1.282 → 1.401 → 1.500 |
| Card SNAI (con logo e testi) | 82–92 | Pulse a due rimbalzi: 1,27× (f84) → 0,85× (f87) → 1,0 (f88) → 1,1× (f89–91) → 1,0 (f93) |
| Card bet365 e WH in fase 3 | 72–112 | Ferme, nessun pulse |
| CTA | tutta la durata | Pulse originale, da lasciare invariato |

## 5. Cosa si può fare subito e cosa è bloccato

| Correzione | Richiede sfondo? | Stato |
|---|---|---|
| Importi già al valore finale dopo l'ingresso | No, solo l'interno della card (tinta piatta 5,6,10) | Fattibile |
| Logo, "FINO A" e importo uniformi dentro le card | No, se la card contiene il nuovo contenuto | Fattibile |
| Card bet365 e WH allargate a 169 px | No, coprono più sfondo senza scoprirne | Fattibile |
| Rimozione del pulse SNAI (f82–92) | Sì, un anello nel fondo scuro, ricavabile dai frame 81 e 93 | Fattibile |
| **Card SNAI da 149 a 118 px di altezza** | **Sì, le strisce della vecchia card, nei frame 65–126** | **Bloccato** |
| Misure target anche nelle fasi 1–2 (card ~165×148) | Sì, le card si restringono sopra pallone e rete in movimento | Bloccato e da chiarire (vedi punto 6) |

## 6. Cosa serve per ripartire (una delle opzioni A–C)

- **A (consigliata).** Un progetto sorgente (AE/Figma/HTML5) oppure la clip di sfondo senza
  card. Con questo la correzione diventa deterministica, senza nulla di inventato.
- **B.** Approvare esplicitamente una ricostruzione dello sfondo nelle strisce, dichiarata come
  inferita. Nei frame 73–112 sarebbe invisibile. Nei frame 66–72 e 113–126 il rischio di
  artefatti è alto e andrebbe valutato su un test dedicato.
- **C.** Accettare una variante che non scopre sfondo: tutte le card larghe 169 px, bet365 e
  WH alte 120, SNAI resta alta 149, spaziatura uniforme di 11 px, contenuti uniformati. Non
  rispetta il requisito "SNAI della stessa dimensione".

Da confermare comunque:
1. Le misure target (21/10/39) valgono anche per le fasi WH solo e bet365+WH, dove oggi le
   card sono più grandi?
2. Sono disponibili i loghi ufficiali bet365, SNAI e William Hill? Oggi esistono solo come
   ritagli da un video a 300 px, quindi asset provvisori.
3. Qual è il font degli importi e di "FINO A"? Non è identificato. Senza font, gli importi
   finali vanno ricavati dal frame di riposo come sagome (`outlined`).

Resto fermo in attesa di una decisione. Non propago nulla ad altri formati.
