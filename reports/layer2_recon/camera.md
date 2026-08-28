# Ricognizione layer 2 — progetti di legge della Camera

Eseguito: 2026-08-27T23:31:02+0200
Comando: `python scripts/run_camera_spike.py`
Endpoint: <https://dati.camera.it/sparql> (SPARQL pubblico, nessuno scraping)

## Resa e costo

| legislatura | atti | righe SPARQL | richieste | secondi |
| --- | --- | --- | --- | --- |
| 18 | 3,757 | 10,392 | 11 | 10.9 |
| 19 | 3,108 | 7,384 | 8 | 7.3 |

## Cosa esce

- atti totali: **6,865**
- con gruppo parlamentare del primo firmatario: **5,824** (84.8%)
- titolo: mediana **161 caratteri**, min 23, max 1,698

### Per iniziativa

| iniziativa | atti | % |
| --- | --- | --- |
| Parlamentare | 5,939 | 86.5% |
| Governo | 668 | 9.7% |
| Regioni | 139 | 2.0% |
| CNEL | 75 | 1.1% |
| Popolare | 39 | 0.6% |
| (assente) | 2 | 0.0% |
| Mista (Governo, Parlamentare, Regioni) | 2 | 0.0% |
| Mista (Governo, Parlamentare) | 1 | 0.0% |

### Primi 15 gruppi

| gruppo | atti |
| --- | --- |
| (assente) | 1,041 |
| MOVIMENTO 5 STELLE | 938 |
| LEGA - SALVINI PREMIER | 936 |
| FRATELLI D'ITALIA | 839 |
| MISTO | 664 |
| PARTITO DEMOCRATICO | 585 |
| PARTITO DEMOCRATICO - ITALIA DEMOCRATICA E PROGRESSISTA | 484 |
| FORZA ITALIA - BERLUSCONI PRESIDENTE | 482 |
| FORZA ITALIA - BERLUSCONI PRESIDENTE - PPE | 274 |
| INSIEME PER IL FUTURO | 112 |
| ITALIA VIVA | 106 |
| AZIONE - ITALIA VIVA - RENEW EUROPE | 94 |
| ALLEANZA VERDI E SINISTRA | 75 |
| NOI MODERATI | 56 |
| NOI MODERATI (NOI CON L'ITALIA, CORAGGIO ITALIA, UDC, ITALIA AL CENTRO)-MAIE | 53 |

## Limiti

- Il **gruppo** è quello del primo firmatario, non del provvedimento: un
  atto firmato da più gruppi risulta attribuito a uno solo.
- I nomi dei gruppi **cambiano fra legislature**: "PARTITO DEMOCRATICO"
  e "PARTITO DEMOCRATICO - ITALIA DEMOCRATICA E PROGRESSISTA" sono lo
  stesso partito e contano separatamente, come Forza Italia con e senza
  "- PPE". Aggregare per partito richiede una mappatura verso chiavi
  canoniche: quella del layer 1 sta in `config/viminale_liste.json` e va
  estesa qui, non duplicata.
- Gli atti di iniziativa governativa non hanno primo firmatario
  parlamentare, quindi non hanno gruppo: vanno letti come governo, non
  come partito.
- Il testo tematizzabile è il **titolo**. Alla Camera è una frase
  descrittiva completa, ma resta molto più corto di un articolo di
  stampa: un topic model tarato sul layer 3 non si applica tale e quale.
- Presentare un DDL non è approvarlo. Questo dataset misura ciò che un
  gruppo *propone*, non ciò che il Parlamento *decide*.
