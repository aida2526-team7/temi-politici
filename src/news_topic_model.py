"""Classificatore esplorativo dei temi della copertura mediatica.

Legge il full-text Media Cloud e produce file di revisione per la validazione
umana: un topic NMF non e' ancora un macrotema. Lo script e' la fonte di verita'
del classificatore; il notebook di orchestrazione lo richiama senza duplicarne la
logica.

Esempio:
    python src/news_topic_model.py --n-topics 12
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "raw" / "mediacloud_fulltext.jsonl"
DEFAULT_OUTPUT_DIR = ROOT / "data" / "processed"
REQUIRED_COLUMNS = {"url", "domain", "seendate", "title", "text"}

# Parole funzione italiane. Lista esplicita e nel repository di proposito: e'
# verificabile a colpo d'occhio e non aggiunge una dipendenza per 300 stringhe.
#
# Perche' e' lunga cosi'. La versione precedente ne aveva 44, scelte a mano, e
# non conteneva si, ma, da, al, le, dei, dell, nel, alla. Risultato misurato sul
# primo giro: i topic 1 e 9 — il 62% del corpus — erano fatti esattamente di
# quelle parole ("si, ma, da, al, le, se, ci, chi, alla" e "dei, le, dell, da,
# al, si"). Non significano niente e assorbono la maggioranza dei documenti.
#
# scikit-learn non ha una lista italiana (`stop_words="italian"` non esiste);
# questa segue quella di NLTK, con le forme senza accento che servono perche'
# TfidfVectorizer usa strip_accents="unicode".
#
# Regola invariata: qui entrano solo parole funzione e termini non tematici.
# Nessuna parola politica sostantiva, mai.
STOPWORDS_IT = {
    # articoli, preposizioni, articoli preposizionati.
    # ("i", "e", "a" non ci sono: il token_pattern di TfidfVectorizer scarta gia'
    # i token di un solo carattere.)
    "il", "lo", "la", "gli", "le", "un", "uno", "una", "del", "dello", "della",
    "dei", "degli", "delle", "dell", "al", "allo", "alla", "ai", "agli", "alle",
    "all", "dal", "dallo", "dalla", "dai", "dagli", "dalle", "nel", "nello",
    "nella", "nei", "negli", "nelle", "sul", "sullo", "sulla", "sui", "sugli",
    "sulle", "col", "coi", "di", "da", "in", "con", "su", "per", "tra", "fra",
    # forme elise. normalizza_testo toglie gli apostrofi, quindi "dall'Italia"
    # diventa il token "dall": senza queste, le preposizioni articolate rientrano
    # dalla finestra. Misurato: erano fra i primi termini del topic dominante.
    "dall", "nell", "sull", "quell", "quest", "un", "sant", "grand", "bell",
    "anch", "com", "ell", "gl",
    # congiunzioni e comparativi rimasti
    "ad", "ed", "od", "sia", "siano", "ovvero", "nonche", "eppure", "seppure",
    # numerali scritti in lettere: normalizza_testo cancella le cifre, non queste,
    # e un numerale non e' un tema.
    "due", "tre", "quattro", "cinque", "sei", "sette", "otto", "nove", "dieci",
    "venti", "trenta", "quaranta", "cinquanta", "cento", "mille", "milioni",
    "miliardi", "primi", "prime", "secondi", "seconda", "seconde", "terzo",
    "terza", "terzi", "terze",
    # pronomi e determinanti
    "mi", "ti", "ci", "vi", "si", "lui", "lei", "loro", "noi", "voi", "io", "tu",
    "me", "te", "se", "chi", "che", "cui", "cosa", "quale", "quali", "quanto",
    "quanti", "quanta", "quante", "questo", "questa", "questi", "queste", "quello",
    "quella", "quelli", "quelle", "stesso", "stessa", "stessi", "stesse", "altro",
    "altra", "altri", "altre", "tutto", "tutta", "tutti", "tutte", "ogni", "ognuno",
    "qualche", "alcuni", "alcune", "nessuno", "nessuna", "molto", "molti", "molte",
    "poco", "pochi", "poche", "tanto", "tanti", "troppo", "suo", "sua", "suoi",
    "sue", "mio", "mia", "miei", "mie", "nostro", "nostra", "nostri", "nostre",
    "vostro", "vostra", "proprio", "propria", "propri", "proprie",
    # congiunzioni e avverbi
    "ma", "anche", "ancora", "ora", "poi", "gia", "già", "non", "piu", "più",
    "meno", "come", "dove", "quando", "perche", "perché", "pero", "però", "quindi",
    "dunque", "invece", "inoltre", "oltre", "senza", "contro", "verso", "dopo",
    "prima", "sempre", "mai", "solo", "soltanto", "appena", "circa", "cosi",
    "così", "bene", "male", "meglio", "peggio", "sopra", "sotto", "dentro",
    "fuori", "davanti", "dietro", "durante", "mentre", "affinche", "affinché",
    "nonche", "nonché", "ovvero", "oppure", "anzi", "cioe", "cioè", "infatti",
    "intanto", "insomma", "almeno", "magari", "forse", "ecco", "proprio",
    # verbi ausiliari e di servizio (forme piu' frequenti)
    "essere", "sono", "sei", "siamo", "siete", "era", "erano", "eravamo", "sara",
    "sarà", "saranno", "sarebbe", "sarebbero", "stato", "stata", "stati", "state",
    "avere", "ho", "hai", "ha", "abbiamo", "avete", "hanno", "aveva", "avevano",
    "avra", "avrà", "avranno", "avrebbe", "avrebbero", "avuto", "essendo",
    "fare", "fa", "fanno", "fatto", "fatta", "fatti", "faceva", "fara", "farà",
    "puo", "può", "possono", "potrebbe", "potrebbero", "potuto", "deve", "devono",
    "dovrebbe", "dovuto", "viene", "vengono", "venuto", "andare", "va", "vanno",
    "dice", "dicono", "detto", "detta", "dire", "vuole", "vogliono", "voluto",
    "resta", "restano", "rimane", "diventa", "diventano", "trova", "trovano",
    # marcatori di cronaca non tematici
    "oggi", "ieri", "domani", "sera", "mattina", "notte", "anno", "anni", "mese",
    "mesi", "giorno", "giorni", "settimana", "ore", "ora", "volta", "volte",
    "secondo", "primo", "prima", "ultimo", "ultima", "nuovo", "nuova", "nuovi",
    "nuove", "grande", "grandi", "parte", "parti", "caso", "casi", "punto",
    "modo", "cosa", "cose", "via", "senso", "fine", "inizio", "corso",
}


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="JSONL full-text Media Cloud")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="directory degli output CSV")
    parser.add_argument("--n-topics", type=int, default=12, help="numero massimo di topic NMF")
    parser.add_argument("--min-df", type=int, default=3, help="document frequency minima TF-IDF")
    parser.add_argument("--max-df", type=float, default=0.85, help="document frequency massima TF-IDF")
    parser.add_argument("--min-text-chars", type=int, default=300, help="lunghezza minima del testo pulito")
    parser.add_argument("--random-state", type=int, default=42, help="seed riproducibile")
    parser.add_argument("--senza-pulizia", action="store_true",
                        help="salta la rimozione di boilerplate e duplicati "
                             "(serve solo a riprodurre il primo giro, non a lavorare)")
    return parser.parse_args()


def normalizza_testo(value):
    value = "" if pd.isna(value) else str(value).lower()
    value = re.sub(r"https?://\S+|www\.\S+", " ", value)
    value = re.sub(r"[^a-zàèéìòóù\s]", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def load_corpus(path, min_text_chars, pulizia=True):
    """Corpus pronto per il modello. Ritorna (corpus, report_pulizia).

    L'ordine conta: la pulizia del boilerplate viene PRIMA del filtro di lingua e
    prima della soglia sui caratteri. Se si filtra per lingua sul testo sporco,
    40 articoli con titolo in caratteri non latini passano come italiani perche'
    il menu attorno a loro e' italiano — e' quello che e' successo al primo giro.
    """
    if not path.is_file():
        raise FileNotFoundError(
            f"Input non trovato: {path}\n"
            "Eseguire prima mediacloud_spike.py e mediacloud_fulltext.py."
        )

    raw = pd.read_json(path, lines=True)
    missing = REQUIRED_COLUMNS - set(raw.columns)
    if missing:
        raise ValueError(f"Campi mancanti nel JSONL: {sorted(missing)}")

    corpus = raw.drop_duplicates(subset="url").copy()
    corpus["title"] = corpus["title"].fillna("")
    corpus["text"] = corpus["text"].fillna("")

    report = {}
    if pulizia:
        # Toglie i template delle testate, i duplicati che la dedup per URL non
        # vede e ricalcola la lingua sul testo pulito. Vedi src/pulizia_corpus.py.
        from pulizia_corpus import pulisci
        records = corpus.to_dict("records")
        records, report = pulisci(records, min_chars=min_text_chars)
        if not records:
            raise ValueError("La pulizia non ha lasciato nessun documento: rivedere le soglie.")
        corpus = pd.DataFrame(records)

    if "language" in corpus.columns:
        corpus = corpus[corpus["language"].fillna("it").eq("it")].copy()
    else:
        corpus["language"] = "unknown"
    if "chars" not in corpus.columns:
        corpus["chars"] = corpus["text"].fillna("").str.len()

    corpus["testo_modello"] = (corpus["title"] + " " + corpus["text"]).map(normalizza_testo)
    corpus = corpus[corpus["testo_modello"].str.len() >= min_text_chars].copy()
    if len(corpus) < 10:
        raise ValueError("Corpus insufficiente: servono almeno 10 articoli con testo valido.")
    return corpus, report


def build_topics(corpus, requested_topics, min_df, max_df, random_state):
    effective_min_df = min(min_df, max(1, len(corpus) // 10))
    vectorizer = TfidfVectorizer(
        stop_words=sorted(STOPWORDS_IT),
        ngram_range=(1, 2),
        min_df=effective_min_df,
        max_df=max_df,
        sublinear_tf=True,
        strip_accents="unicode",
    )
    matrix = vectorizer.fit_transform(corpus["testo_modello"])
    if matrix.shape[1] < 2:
        raise ValueError("Vocabolario insufficiente: controllare corpus e parametri TF-IDF.")

    n_topics = min(requested_topics, len(corpus) - 1, matrix.shape[1] - 1)
    if n_topics < 2:
        raise ValueError("Servono almeno due topic stimabili.")

    model = NMF(n_components=n_topics, init="nndsvda", random_state=random_state, max_iter=500)
    weights = model.fit_transform(matrix)
    return model, weights, vectorizer.get_feature_names_out(), matrix.shape, n_topics, effective_min_df


def topic_terms(components, features, dominant_counts, n_terms=12):
    rows = []
    for topic_id, component in enumerate(components):
        top = component.argsort()[-n_terms:][::-1]
        rows.append(
            {
                "topic_id": topic_id,
                "articoli_dominanti": int(dominant_counts.get(topic_id, 0)),
                "termini_caratteristici": ", ".join(features[index] for index in top),
                "macrotema_validato": "",
                "note_revisione": "",
            }
        )
    return pd.DataFrame(rows)


def export_results(corpus, model, weights, features, output_dir, metadata):
    output_dir.mkdir(parents=True, exist_ok=True)
    topic_ids = weights.argmax(axis=1)
    corpus["estratto"] = corpus["text"].str.replace(r"\s+", " ", regex=True).str.slice(0, 500)
    weight_columns = [f"topic_{topic_id}_peso" for topic_id in range(weights.shape[1])]
    review = corpus[["url", "domain", "seendate", "title", "language", "chars", "estratto"]].join(
        pd.DataFrame(weights, columns=weight_columns, index=corpus.index)
    )
    review["topic_id"] = topic_ids
    review["confidenza_topic"] = weights.max(axis=1) / weights.sum(axis=1).clip(min=1e-12)

    counts = pd.Series(topic_ids).value_counts().to_dict()
    terms = topic_terms(model.components_, features, counts)
    review = review.merge(terms[["topic_id", "termini_caratteristici"]], on="topic_id", how="left")
    review = review.sort_values(["topic_id", "confidenza_topic"], ascending=[True, False])

    review_path = output_dir / "news_topic_review.csv"
    terms_path = output_dir / "news_topic_terms.csv"
    metadata_path = output_dir / "topic_model_metadata.json"
    review.to_csv(review_path, index=False, encoding="utf-8-sig")
    terms.to_csv(terms_path, index=False, encoding="utf-8-sig")
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    return review_path, terms_path, metadata_path, terms


def main():
    args = parse_args()
    if args.n_topics < 2:
        raise ValueError("--n-topics deve essere almeno 2")
    corpus, report_pulizia = load_corpus(args.input, args.min_text_chars,
                                         pulizia=not args.senza_pulizia)
    model, weights, features, shape, n_topics, effective_min_df = build_topics(
        corpus, args.n_topics, args.min_df, args.max_df, args.random_state
    )
    metadata = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "input": str(args.input),
        "articles": int(len(corpus)),
        "tfidf_shape": list(shape),
        "n_topics": n_topics,
        "requested_n_topics": args.n_topics,
        "min_df": effective_min_df,
        "max_df": args.max_df,
        "random_state": args.random_state,
        # Cosa e' stato tolto prima di modellare: senza, i topic non sono
        # confrontabili fra un giro e l'altro.
        "pulizia": report_pulizia,
        "stopwords": len(STOPWORDS_IT),
    }
    review_path, terms_path, metadata_path, terms = export_results(
        corpus, model, weights, features, args.output_dir, metadata
    )
    print(f"Corpus analizzato: {len(corpus):,} articoli")
    print(f"Matrice TF-IDF: {shape[0]:,} articoli x {shape[1]:,} termini | topic: {n_topics}")
    print("\nTopic da validare:")
    print(terms[["topic_id", "articoli_dominanti", "termini_caratteristici"]].to_string(index=False))
    print("\nOutput creati:")
    for path in (review_path, terms_path, metadata_path):
        print(f" - {path}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (FileNotFoundError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(2)
