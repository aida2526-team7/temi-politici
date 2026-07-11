# Politica 3D — Analisi della comunicazione politica italiana

Progetto di master (Big Data Processing & Data Engineering), gruppo di 4 persone.
Questo README è il documento di riferimento: visione, ipotesi, fonti, architettura della pipeline, stato delle decisioni.

---

## 1. Visione

Dashboard di supporto decisionale per l'analisi della comunicazione politica italiana su tre piani:

1. **Cosa dicono** — temi della comunicazione di partito (siti web, programmi elettorali)
2. **Cosa fanno** — produzione legislativa (disegni di legge presentati)
3. **Chi li sostiene** — risultati elettorali (+ eventualmente finanziamenti, modulo opzionale)

L'output decisionale sono i **disallineamenti fra i tre piani**, letti come segnali:
- per il proprio partito: rischi di coerenza da correggere
- per gli avversari: vulnerabilità
- per gli analisti: indicatori anticipatori di instabilità

Il taglio è *decision support per chi progetta comunicazione politica*, non data journalism / accountability. La differenza sta nella domanda: non "guarda cosa hanno fatto" ma "cosa conviene fare". Naming coerente con questo taglio: "indice di coerenza programmatica", "segnali anticipatori di riposizionamento" — non "tracker delle promesse".

## 2. Ipotesi di ricerca

Verificabili con i dati previsti, in ordine di solidità:

- **H1 — Coerenza programmatica**: lo scostamento fra temi dichiarati in campagna e temi dei DDL presentati in legislatura varia per partito ed è misurabile. (Descrittiva, la più solida.)
- **H2 — Coerenza → consenso**: lo scostamento H1 correla con la variazione di consenso alle elezioni successive. (Correlazionale, esplorativa.)
- **H3 — Early warning**: shift tematici improvvisi nella comunicazione di un partito di maggioranza anticipano eventi di instabilità (crisi di governo, rimpasti). Serie temporale a granularità giornaliera via Media Cloud. (Esplorativa.)
- **H4 (opzionale) — Finanziamenti**: i flussi di finanziamento (2×1000, erogazioni liberali) anticipano o seguono gli spostamenti tematici. (La più speculativa; modulo di fase 2, dichiarato ma non critico per la consegna.)

Il sentiment è declassato a segnale accessorio: eventualmente testare se anticipa lo spostamento tematico. Non è un predittore del voto (bias di selezione, sentiment ≠ intenzione di voto — letteratura da Gayo-Avello in poi).

## 3. Fonti dati

| Fonte | Layer | Accesso | Stato |
|---|---|---|---|
| Media Cloud | Copertura mediatica (stampa) | API interrogabile (`mediacloud_spike.py` → `mediacloud_fulltext.py`) | Spike 1 **fatto**: fonti più pulite di GDELT, copertura per partito misurata. GDELT scartato (tag `Themes` troppo rumorosi sull'italiano) |
| Wayback Machine (CDX API) | Comunicazione di partito nel tempo | Scraping snapshot pagine programmatiche, 6-8 partiti principali | **Da scrivere**; copertura snapshot per partito/anno da censire (spike 2) |
| Programmi elettorali depositati | Ground truth temi dichiarati | Documenti ufficiali, stabili | Complementare a Wayback, non sostitutivo |
| MARPOR / Comparative Manifesto Project | Validazione esterna del topic modeling | Dataset accademico, codifica manuale dei programmi | Copertura sulle elezioni scelte **da verificare** |
| dati.camera.it + dati.senato.it | Produzione legislativa (DDL) | Endpoint SPARQL pubblici: titolo, abstract, presentatori, gruppo, date, iter | **Da scrivere**; niente scraping. Timeout su query pesanti da misurare (spike 3) |
| Eligendo (Min. Interno) | Risultati elettorali | Download, granularità comunale | Formato e granularità effettiva da verificare (spike 4) |
| MEF / Camera (2×1000, erogazioni liberali) | Finanziamenti (opzionale, H4) | Dati pubblici; 2×1000 aggregato per partito, erogazioni sopra soglia nominali | Granularità determina cosa è correlabile; verificare prima di promettere il modulo |

### Note sulle fonti
- I siti dei partiti cambiano struttura nel tempo: **parsing per epoca**, non template unico.
- Media Cloud dà solo metadati (url/titolo/data/fonte), non il full-text: il testo lo scarica l'harvester, poi la NLP nostra (topic + sentiment) lavora sul testo vero. Niente tassonomia precotta da ripulire come in GDELT.
- Social scartati: X/Twitter API fuori budget; YouTube/Telegram eventualmente solo se il sentiment rientra come modulo accessorio.

## 4. Ontologia tematica comune

**Artefatto critico del progetto.** 10-15 macro-categorie definite a mano, partendo dalle categorie MARPOR ridotte (aggancio a standard accademico). È il contratto fra i tre layer: le tre tassonomie di partenza (topic dei media via Media Cloud, topic della comunicazione di partito, categorie DDL) convergono qui.

**Va congelata prima di scrivere qualsiasi trasformazione.**

## 5. Decisioni prese e aperte

**Prese:**
- Granularità della correlazione elettorale: **temporale/nazionale** (coerente col taglio 3D; la granularità comunale serviva al sentiment, declassato).
- Finestra temporale proposta: **2018 → 2026** (due politiche, europee, più cambi di governo per H3). Da confermare a fine spike.
- Sentiment: fuori dal core, eventuale modulo accessorio.
- Finanziamenti (H4): modulo opzionale di fase 2.

**Aperte:**
- Conferma finestra temporale (dipende da copertura Wayback e MARPOR).
- Elenco definitivo partiti (proposta: 6-8 principali).
- Peso valutazione docente: architettura vs analisi → determina allocazione effort. **Da chiedere prima di tutto.**

## 6. Piano di lavoro

### Fase 0 — Spike di validazione (1 settimana, uno a testa)
1. **Media Cloud** (fatto): campione di URL sulla collezione Italia → mix delle fonti + copertura per partito. Esito: GDELT scartato (tag `Themes` troppo rumorosi sull'italiano); si usa Media Cloud come discovery e la NLP nostra sul full-text scaricato.
2. **Wayback CDX**: censimento snapshot pagine programmatiche per 6-8 partiti → matrice partito×anno di copertura.
3. **SPARQL Camera/Senato**: query di prova su una legislatura → schema dati reali, volumetrie, comportamento timeout.
4. **Eligendo**: download risultati sulla finestra → formato e granularità effettiva.

### Fase 1 — Ontologia tematica (in parallelo a fase 0, tutti insieme)
Le 10-15 macro-categorie. Congelate a fine fase.

### Fase 2 — Ingestion (bronze)
Tre pipeline indipendenti, solo download raw, zero trasformazioni.

### Fase 3 — Processing (silver)
Parsing, pulizia, mapping sull'ontologia. Topic modeling e inferenza. Fase più lunga.

### Fase 4 — Serving (gold + dashboard)
Tabelle aggregate per gli indici + dashboard.

## 7. Architettura della pipeline (ipotesi, no codice)

Architettura **medallion** (bronze/silver/gold), nominata esplicitamente così anche in presentazione.

### Bronze — Ingestion
Tre pipeline batch indipendenti e idempotenti. Salvano il raw così com'è, partizionato per fonte/data su object storage o filesystem.

- **`mediacloud-harvester`** (`mediacloud_spike.py` + `mediacloud_fulltext.py`): discovery per partito sulla collezione Italia → URL → full-text via harvester, con ripassata anti-sport e copertura per partito sul corpus pulito.
- **`wayback-harvester`** (da scrivere): interroga la CDX API per gli URL programmatici di ciascun partito, scarica gli snapshot HTML con timestamp. Idempotente per (URL, timestamp snapshot).
- **`parliament-harvester`** (da scrivere): query SPARQL paginategli su dati.camera.it e dati.senato.it, salva JSON raw dei DDL. Idempotente per ID atto.
- **`elections-loader`** (da scrivere): download one-shot da Eligendo, CSV raw.

### Silver — Processing
- **`news-topic-mapper`**: sul full-text degli articoli Media Cloud, topic modeling + mapping sull'ontologia. Output: serie temporale giornaliera tema×fonte.
- **`party-corpus-builder`**: parsing HTML degli snapshot (parser per epoca), estrazione testo, dedup fra snapshot consecutivi identici.
- **`topic-modeler`**: BERTopic (o simile) sul corpus partiti; mapping cluster → ontologia (supervisione manuale del mapping). Validazione contro MARPOR dove disponibile.
- **`ddl-classifier`**: inferenza del topic model su titolo+abstract dei DDL. Output: distribuzione temi per partito per periodo.
- **`elections-normalizer`**: risultati per partito per elezione, serie storica nazionale.

### Gold — Serving
Tabelle aggregate per gli indici:
- **Indice di coerenza programmatica** (H1): distanza fra distribuzione temi in campagna e distribuzione temi nei DDL, per partito per legislatura.
- **Coerenza × consenso** (H2): join con delta elettorale.
- **Shift tematico / early warning** (H3): variazioni brusche nella serie giornaliera della copertura Media Cloud + serie comunicazione partito, allineate con timeline eventi di governo.

### Dashboard
Sopra il gold layer. Viste: evoluzione temi per partito, indice di coerenza comparato, timeline shift tematici vs eventi politici, (opzionale) flussi finanziamenti.

### Orchestrazione
**Dagster** (preferito ad Airflow per leggerezza di setup) invece di script in cron. Upgrade architetturale col miglior rapporto costo/impressione in sede di valutazione.

### Storage
- Bronze: filesystem/object storage partizionato per fonte/data
- Silver/Gold: da decidere (candidati: DuckDB/Parquet per semplicità, o PostgreSQL se serve la dashboard live)

## 8. Primo passo operativo

Lo spike CDX (Wayback) è il pezzo con più incognite e nessun riuso: script di censimento snapshot per i siti dei partiti → matrice partito×anno.
