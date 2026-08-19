# Ricognizione layer "chi li sostiene" — risultati elettorali

Eseguito: 2026-08-19T20:15:05+0200
Comando: `python scripts/run_eligendo_spike.py`
Fonte: <https://dait.interno.gov.it/daithome/documenti/opendata/catalogoagid/> (catalogo AgID del Viminale, download diretto)

## Cosa c'è, e a che costo

| consultazione | data | righe | comuni | liste | voti di lista | secondi |
| --- | --- | --- | --- | --- | --- | --- |
| camera2022 | 2022-09-25 | 117,591 | 7,824 | 23 | 27,069,655 | 2.3 |
| europee2024 | 2024-06-09 | 93,984 | 7,891 | 15 | 23,290,624 | 2.1 |
| senato2022 | 2022-09-25 | 117,510 | 7,545 | 22 | 26,601,426 | 2.7 |

### camera2022 — prime 10 liste

| lista | voti | % |
| --- | --- | --- |
| FRATELLI D'ITALIA CON GIORGIA MELONI | 7,098,555 | 26.22% |
| PARTITO DEMOCRATICO - ITALIA DEMOCRATICA E PROGRESSISTA | 5,128,861 | 18.95% |
| MOVIMENTO 5 STELLE | 4,178,360 | 15.44% |
| LEGA PER SALVINI PREMIER | 2,392,976 | 8.84% |
| FORZA ITALIA | 2,218,466 | 8.20% |
| AZIONE - ITALIA VIVA - CALENDA | 2,065,444 | 7.63% |
| ALLEANZA VERDI E SINISTRA | 972,919 | 3.59% |
| +EUROPA | 759,872 | 2.81% |
| ITALEXIT PER L'ITALIA | 516,465 | 1.91% |
| UNIONE POPOLARE CON DE MAGISTRIS | 378,959 | 1.40% |

### europee2024 — prime 10 liste

| lista | voti | % |
| --- | --- | --- |
| FRATELLI D'ITALIA | 6,713,364 | 28.82% |
| PARTITO DEMOCRATICO | 5,609,327 | 24.08% |
| MOVIMENTO 5 STELLE | 2,326,500 | 9.99% |
| FORZA ITALIA - NOI MODERATI - PPE | 2,238,962 | 9.61% |
| LEGA SALVINI PREMIER | 2,096,486 | 9.00% |
| ALLEANZA VERDI E SINISTRA | 1,562,606 | 6.71% |
| STATI UNITI D'EUROPA | 875,806 | 3.76% |
| AZIONE - SIAMO EUROPEI | 778,628 | 3.34% |
| PACE TERRA DIGNITA' | 513,881 | 2.21% |
| LIBERTA' | 284,577 | 1.22% |

### senato2022 — prime 10 liste

| lista | voti | % |
| --- | --- | --- |
| FRATELLI D'ITALIA CON GIORGIA MELONI | 6,975,727 | 26.22% |
| PARTITO DEMOCRATICO - ITALIA DEMOCRATICA E PROGRESSISTA | 5,019,511 | 18.87% |
| MOVIMENTO 5 STELLE | 4,128,240 | 15.52% |
| LEGA PER SALVINI PREMIER | 2,371,657 | 8.92% |
| FORZA ITALIA | 2,223,392 | 8.36% |
| AZIONE - ITALIA VIVA - CALENDA | 2,016,702 | 7.58% |
| ALLEANZA VERDI E SINISTRA | 933,196 | 3.51% |
| +EUROPA | 776,455 | 2.92% |
| ITALEXIT PER L'ITALIA | 497,741 | 1.87% |
| UNIONE POPOLARE CON DE MAGISTRIS | 351,640 | 1.32% |

## Limiti

- **Le politiche 2018 non sono in questo catalogo.** Verificato:
  `Camera_Italia_LivComune.csv` contiene il 2022, non il 2018, ed è lo
  stesso file di `camera-2022-Italia-livcomune.csv`. Senza il 2018 la
  finestra del piano (2018→2026) copre una sola politica: H2 può
  confrontare al massimo 2022 con le europee 2024. Il 2018 va cercato
  nell'archivio storico Eligendo, che non espone CSV diretti.
- **Valle d'Aosta assente** dai file `Italia`: ha un file separato, come
  il Trentino per il Senato. I totali qui sotto sono quindi leggermente
  sotto quelli ufficiali e **vanno riconciliati** con la pubblicazione
  del Viminale prima di essere usati in un indice.
- La **percentuale è sui voti di lista validi**, non sui votanti: schede
  bianche, nulle e contestate non sono attribuite a nessuna lista.
- I file sono a **livello comunale**; qui si aggrega a nazionale perché è
  la granularità decisa dal piano. Il dettaglio comunale resta
  disponibile se la decisione cambia.
- Le **liste non sono i partiti**: "AZIONE - ITALIA VIVA - CALENDA" nel
  2022 e "AZIONE - SIAMO EUROPEI" nel 2024 sono cartelli diversi. Serve
  la stessa mappatura verso chiavi canoniche già richiesta dal layer 2.
