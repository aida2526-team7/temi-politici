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

# Piccola lista trasparente: puo' crescere solo con termini non tematici emersi
# nella revisione, non con parole politiche sostantive.
STOPWORDS_IT = {
    "anche", "ancora", "avere", "come", "con", "contro", "dalla", "dalle", "dello",
    "della", "delle", "dopo", "essere", "fatto", "fare", "gli", "ha", "hanno",
    "legge", "nelle", "non", "ogni", "per", "perche", "perché", "piu", "più",
    "quale", "quello", "questa", "questo", "sara", "sarà", "sono", "sua", "sue",
    "sul", "sulla", "tutti", "una", "uno", "verso", "oggi", "ieri", "dice", "secondo",
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
    return parser.parse_args()


def normalizza_testo(value):
    value = "" if pd.isna(value) else str(value).lower()
    value = re.sub(r"https?://\S+|www\.\S+", " ", value)
    value = re.sub(r"[^a-zàèéìòóù\s]", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def load_corpus(path, min_text_chars):
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
    if "language" in corpus.columns:
        corpus = corpus[corpus["language"].fillna("it").eq("it")].copy()
    else:
        corpus["language"] = "unknown"
    if "chars" not in corpus.columns:
        corpus["chars"] = corpus["text"].fillna("").str.len()

    corpus["title"] = corpus["title"].fillna("")
    corpus["text"] = corpus["text"].fillna("")
    corpus["testo_modello"] = (corpus["title"] + " " + corpus["text"]).map(normalizza_testo)
    corpus = corpus[corpus["testo_modello"].str.len() >= min_text_chars].copy()
    if len(corpus) < 10:
        raise ValueError("Corpus insufficiente: servono almeno 10 articoli con testo valido.")
    return corpus


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
    corpus = load_corpus(args.input, args.min_text_chars)
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
