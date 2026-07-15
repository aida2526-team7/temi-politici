"""Campionamento riproducibile per lo human check dei topic NMF.

Il modulo seleziona record dagli output esistenti senza modificare input o modello.
Selezione, validazione, presentazione e scrittura restano funzioni separate.
"""

from __future__ import annotations

import hashlib
import json
import platform
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


BASE_COLUMNS = {
    "url", "domain", "seendate", "title", "estratto", "topic_id",
    "confidenza_topic", "termini_caratteristici",
}
HUMAN_COLUMNS = [
    "classificazione_umana",
    "etichetta_tema_proposta",
    "boilerplate_si_no",
    "duplicato_sospetto_si_no",
    "decisione_inclusione",
    "note_revisore",
]
SELECTION_TYPES = {"top_weight", "random_seed_42", "artifact_check"}
OUTPUT_COLUMNS = [
    "review_id", "source_row_index", "topic_id", "tipo_selezione",
    "selection_rank", "domain", "seendate", "title", "url", "estratto",
    "peso_topic_dominante", "confidenza_topic", "termini_caratteristici",
    "valutazione_preliminare", *HUMAN_COLUMNS,
]


@dataclass(frozen=True)
class SelectionResult:
    """Campione e deroghe prodotte dalla selezione, prima della scrittura."""

    sample: pd.DataFrame
    exceptions: tuple[dict[str, Any], ...]


def find_repo_root(start: Path | None = None) -> Path:
    """Trova la root Git a partire da un file o da una directory."""

    current = (start or Path.cwd()).resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    raise FileNotFoundError("Root Git non trovata")


def resolve_repo_path(repo_root: Path, relative_path: str) -> Path:
    """Risolve un percorso relativo impedendo uscite dalla root."""

    raw = Path(relative_path)
    if raw.is_absolute():
        raise ValueError(f"Il percorso deve essere relativo: {relative_path}")
    resolved = (repo_root / raw).resolve()
    try:
        resolved.relative_to(repo_root.resolve())
    except ValueError as error:
        raise ValueError(f"Il percorso esce dalla root: {relative_path}") from error
    return resolved


def load_config(config_path: Path, repo_root: Path) -> dict[str, Any]:
    """Carica e valida tutti i parametri espliciti della selezione."""

    config = json.loads(config_path.read_text(encoding="utf-8"))
    required = {
        "input_review_csv", "input_topic_terms_csv", "output_directory",
        "random_seed", "topic_utili", "topic_artefatto", "top_weight_per_topic",
        "random_per_topic", "artifact_checks_per_topic",
        "max_same_domain_per_topic", "excerpt_max_chars", "encoding",
        "categorie_di_revisione",
    }
    missing = required - set(config)
    if missing:
        raise ValueError(f"Configurazione incompleta: {sorted(missing)}")
    for key in ("input_review_csv", "input_topic_terms_csv", "output_directory"):
        resolve_repo_path(repo_root, str(config[key]))
    useful = [int(value) for value in config["topic_utili"]]
    artifacts = [int(value) for value in config["topic_artefatto"]]
    if set(useful) & set(artifacts):
        raise ValueError("topic_utili e topic_artefatto devono essere disgiunti")
    if len(useful) != len(set(useful)) or len(artifacts) != len(set(artifacts)):
        raise ValueError("Gli identificativi dei topic devono essere univoci")
    for key in (
        "top_weight_per_topic", "random_per_topic", "artifact_checks_per_topic",
        "max_same_domain_per_topic", "excerpt_max_chars",
    ):
        if int(config[key]) <= 0:
            raise ValueError(f"{key} deve essere positivo")
    return config


def topic_weight_columns(frame: pd.DataFrame) -> list[str]:
    """Individua e ordina numericamente le colonne `topic_N_peso`."""

    indexed: list[tuple[int, str]] = []
    for column in frame.columns:
        text = str(column)
        if text.startswith("topic_") and text.endswith("_peso"):
            middle = text[len("topic_"):-len("_peso")]
            if middle.isdigit():
                indexed.append((int(middle), text))
    indexed.sort()
    return [column for _, column in indexed]


def validate_inputs(review: pd.DataFrame, terms: pd.DataFrame, config: Mapping[str, Any]) -> list[str]:
    """Valida schema, topic richiesti e disponibilità delle colonne peso."""

    missing = BASE_COLUMNS - set(review.columns)
    if missing:
        raise ValueError(f"Colonne obbligatorie mancanti nel review CSV: {sorted(missing)}")
    term_missing = {"topic_id", "termini_caratteristici"} - set(terms.columns)
    if term_missing:
        raise ValueError(f"Colonne obbligatorie mancanti nel topic terms CSV: {sorted(term_missing)}")
    weights = topic_weight_columns(review)
    if not weights:
        raise ValueError("Nessuna colonna topic_N_peso trovata")
    expected = [f"topic_{index}_peso" for index in range(len(weights))]
    if weights != expected:
        raise ValueError(f"Colonne peso non continue: attese {expected}, trovate {weights}")
    requested = set(map(int, config["topic_utili"])) | set(map(int, config["topic_artefatto"]))
    missing_topics = requested - set(pd.to_numeric(review["topic_id"], errors="raise").astype(int))
    missing_terms = requested - set(pd.to_numeric(terms["topic_id"], errors="raise").astype(int))
    if missing_topics:
        raise ValueError(f"Topic richiesti assenti dal review CSV: {sorted(missing_topics)}")
    if missing_terms:
        raise ValueError(f"Topic richiesti assenti dal topic terms CSV: {sorted(missing_terms)}")
    return weights


def load_inputs(
    review_path: Path,
    terms_path: Path,
    config: Mapping[str, Any],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Carica gli input senza modificarli e conserva l'indice della riga sorgente."""

    encoding = str(config["encoding"])
    if not review_path.is_file() or not terms_path.is_file():
        missing = [str(path.name) for path in (review_path, terms_path) if not path.is_file()]
        raise FileNotFoundError(f"Input mancanti: {missing}")
    review = pd.read_csv(review_path, encoding=encoding, low_memory=False)
    terms = pd.read_csv(terms_path, encoding=encoding, low_memory=False)
    validate_inputs(review, terms, config)
    review = review.copy()
    review.insert(0, "source_row_index", review.index.astype(int))
    term_map = terms.drop_duplicates("topic_id").set_index("topic_id")["termini_caratteristici"]
    review["termini_caratteristici"] = review["topic_id"].map(term_map).fillna(review["termini_caratteristici"])
    return review, terms


def duplicate_key(frame: pd.DataFrame) -> pd.Series:
    """Costruisce la chiave esatta titolo più estratto usata per la deduplica."""

    return frame["title"].fillna("").astype(str) + "\x1f" + frame["estratto"].fillna("").astype(str)


def exclude_title_excerpt_duplicates(frame: pd.DataFrame) -> pd.DataFrame:
    """Mantiene una sola riga sorgente per ogni coppia esatta titolo–estratto."""

    working = frame.copy()
    working["_duplicate_key"] = duplicate_key(working)
    return working.drop_duplicates("_duplicate_key", keep="first").copy()


def diversify_by_domain(
    candidates: pd.DataFrame,
    count: int,
    domain_counts: dict[str, int],
    max_same_domain: int,
) -> tuple[pd.DataFrame, dict[str, int], bool]:
    """Seleziona righe preferendo domini meno usati e rispettando il limite."""

    remaining = candidates.copy()
    selected_rows: list[pd.Series] = []
    counts = dict(domain_counts)
    while len(selected_rows) < int(count) and not remaining.empty:
        eligible = remaining[
            remaining["domain"].fillna("[MISSING]").astype(str).map(lambda value: counts.get(value, 0) < int(max_same_domain))
        ]
        if eligible.empty:
            break
        minimum = min(counts.get(str(value), 0) for value in eligible["domain"].fillna("[MISSING]"))
        preferred = eligible[
            eligible["domain"].fillna("[MISSING]").astype(str).map(lambda value: counts.get(value, 0) == minimum)
        ]
        row = preferred.iloc[0]
        selected_rows.append(row)
        domain = str(row["domain"] if pd.notna(row["domain"]) else "[MISSING]")
        counts[domain] = counts.get(domain, 0) + 1
        remaining = remaining[remaining["source_row_index"] != int(row["source_row_index"])]
    exception_used = False
    while len(selected_rows) < int(count) and not remaining.empty:
        exception_used = True
        row = remaining.iloc[0]
        selected_rows.append(row)
        domain = str(row["domain"] if pd.notna(row["domain"]) else "[MISSING]")
        counts[domain] = counts.get(domain, 0) + 1
        remaining = remaining.iloc[1:]
    if len(selected_rows) != int(count):
        raise ValueError(f"Impossibile selezionare {count} record: disponibili {len(selected_rows)}")
    return pd.DataFrame(selected_rows).reset_index(drop=True), counts, exception_used


def select_top_weight(
    frame: pd.DataFrame,
    topic_id: int,
    count: int,
    used_keys: set[str],
    domain_counts: dict[str, int],
    max_same_domain: int,
) -> tuple[pd.DataFrame, dict[str, int], bool]:
    """Seleziona record ad alto peso con tie-break sull'indice sorgente."""

    column = f"topic_{int(topic_id)}_peso"
    candidates = frame[(frame["topic_id"] == int(topic_id)) & ~frame["_duplicate_key"].isin(used_keys)].copy()
    candidates = candidates.sort_values([column, "source_row_index"], ascending=[False, True])
    return diversify_by_domain(candidates, count, domain_counts, max_same_domain)


def deterministic_sample(
    frame: pd.DataFrame,
    topic_id: int,
    count: int,
    seed: int,
    used_keys: set[str],
    domain_counts: dict[str, int],
    max_same_domain: int,
) -> tuple[pd.DataFrame, dict[str, int], bool]:
    """Campiona senza replacement con seed per-topic e diversificazione domini."""

    candidates = frame[(frame["topic_id"] == int(topic_id)) & ~frame["_duplicate_key"].isin(used_keys)].copy()
    candidates = candidates.sample(frac=1, random_state=int(seed) + int(topic_id)).reset_index(drop=True)
    return diversify_by_domain(candidates, count, domain_counts, max_same_domain)


def select_artifact_checks(
    frame: pd.DataFrame,
    topic_ids: Sequence[int],
    count_per_topic: int,
    used_keys: set[str],
) -> list[pd.DataFrame]:
    """Seleziona controlli artefatto ad alto peso, un topic alla volta."""

    selected: list[pd.DataFrame] = []
    for topic_id in topic_ids:
        column = f"topic_{int(topic_id)}_peso"
        candidates = frame[(frame["topic_id"] == int(topic_id)) & ~frame["_duplicate_key"].isin(used_keys)].copy()
        chosen = candidates.sort_values([column, "source_row_index"], ascending=[False, True]).head(int(count_per_topic))
        if len(chosen) != int(count_per_topic):
            raise ValueError(f"Record insufficienti per il controllo artefatto del topic {topic_id}")
        used_keys.update(chosen["_duplicate_key"].astype(str))
        chosen["tipo_selezione"] = "artifact_check"
        chosen["selection_rank"] = range(1, len(chosen) + 1)
        selected.append(chosen)
    return selected


def build_review_sample(review: pd.DataFrame, config: Mapping[str, Any]) -> SelectionResult:
    """Costruisce il campione completo applicando tutte le regole configurate."""

    frame = exclude_title_excerpt_duplicates(review)
    used_keys: set[str] = set()
    pieces: list[pd.DataFrame] = []
    exceptions: list[dict[str, Any]] = []
    max_domain = int(config["max_same_domain_per_topic"])
    for topic_id in map(int, config["topic_utili"]):
        counts: dict[str, int] = {}
        top, counts, top_exception = select_top_weight(
            frame, topic_id, int(config["top_weight_per_topic"]), used_keys, counts, max_domain
        )
        used_keys.update(top["_duplicate_key"].astype(str))
        top["tipo_selezione"] = "top_weight"
        top["selection_rank"] = range(1, len(top) + 1)
        pieces.append(top)
        random, counts, random_exception = deterministic_sample(
            frame, topic_id, int(config["random_per_topic"]), int(config["random_seed"]), used_keys, counts, max_domain
        )
        used_keys.update(random["_duplicate_key"].astype(str))
        random["tipo_selezione"] = "random_seed_42"
        random["selection_rank"] = range(1, len(random) + 1)
        pieces.append(random)
        if top_exception or random_exception:
            exceptions.append({
                "topic_id": topic_id,
                "rule": "max_same_domain_per_topic",
                "limit": max_domain,
                "reason": "record sufficienti disponibili solo superando il limite",
                "final_domain_counts": counts,
            })
    pieces.extend(select_artifact_checks(
        frame,
        list(map(int, config["topic_artefatto"])),
        int(config["artifact_checks_per_topic"]),
        used_keys,
    ))
    sample = pd.concat(pieces, ignore_index=True)
    sample["peso_topic_dominante"] = [
        row[f"topic_{int(row['topic_id'])}_peso"] for _, row in sample.iterrows()
    ]
    sample["estratto"] = sample["estratto"].fillna("").astype(str).str.slice(0, int(config["excerpt_max_chars"]))
    sample["valutazione_preliminare"] = sample["tipo_selezione"].map({
        "top_weight": "topic utile: caso ad alto peso da verificare",
        "random_seed_42": "topic utile: caso casuale da verificare",
        "artifact_check": "possibile artefatto: caso ad alto peso da verificare",
    })
    for column in HUMAN_COLUMNS:
        sample[column] = ""
    sample["review_id"] = [
        f"T{int(row.topic_id):02d}-{str(row.tipo_selezione).upper()}-{int(row.selection_rank):02d}"
        for row in sample.itertuples(index=False)
    ]
    sample = sample[OUTPUT_COLUMNS].sort_values(
        ["topic_id", "tipo_selezione", "selection_rank"]
    ).reset_index(drop=True)
    validate_sample(sample, config, exceptions)
    return SelectionResult(sample=sample, exceptions=tuple(exceptions))


def validate_sample(
    sample: pd.DataFrame,
    config: Mapping[str, Any],
    exceptions: Sequence[Mapping[str, Any]] = (),
) -> None:
    """Verifica cardinalità, copertura, deduplica, domini e campi umani."""

    expected = (
        len(config["topic_utili"]) * (int(config["top_weight_per_topic"]) + int(config["random_per_topic"]))
        + len(config["topic_artefatto"]) * int(config["artifact_checks_per_topic"])
    )
    if len(sample) != expected:
        raise ValueError(f"Campione di {len(sample)} righe, attese {expected}")
    requested = set(map(int, config["topic_utili"])) | set(map(int, config["topic_artefatto"]))
    if set(sample["topic_id"].astype(int)) != requested:
        raise ValueError("Il campione non copre esattamente i topic richiesti")
    if sample.duplicated(["title", "estratto"]).any():
        raise ValueError("Il campione contiene duplicati titolo + estratto")
    if sample["review_id"].duplicated().any():
        raise ValueError("review_id non univoci")
    if sample["url"].fillna("").astype(str).str.strip().eq("").any():
        raise ValueError("Il campione contiene URL vuoti")
    if not set(sample["tipo_selezione"]).issubset(SELECTION_TYPES):
        raise ValueError("tipo_selezione non ammesso")
    for column in HUMAN_COLUMNS:
        if sample[column].fillna("").astype(str).ne("").any():
            raise ValueError(f"La colonna umana {column} deve essere vuota")
    excepted_topics = {int(item["topic_id"]) for item in exceptions}
    useful = sample[sample["topic_id"].isin(config["topic_utili"])]
    counts = useful.groupby(["topic_id", "domain"], dropna=False).size()
    violations = counts[counts > int(config["max_same_domain_per_topic"])]
    invalid = [int(topic_id) for topic_id, _ in violations.index if int(topic_id) not in excepted_topics]
    if invalid:
        raise ValueError(f"Limite per dominio violato senza eccezione: {sorted(set(invalid))}")


def generate_selection_summary(sample: pd.DataFrame, exceptions: Sequence[Mapping[str, Any]]) -> pd.DataFrame:
    """Genera conteggi per topic e tipo con diversità dei domini."""

    summary = (
        sample.groupby(["topic_id", "tipo_selezione"], sort=True)
        .agg(records=("review_id", "size"), unique_domains=("domain", "nunique"))
        .reset_index()
    )
    exception_topics = {int(item["topic_id"]) for item in exceptions}
    summary["domain_limit_exception"] = summary["topic_id"].isin(exception_topics)
    return summary


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Calcola SHA-256 con lettura streaming."""

    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def _relative(repo_root: Path, path: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def generate_review_guide(config: Mapping[str, Any], exceptions: Sequence[Mapping[str, Any]]) -> str:
    """Genera la guida Markdown per la compilazione umana del CSV."""

    categories = "\n".join(f"- {value}" for value in config["categorie_di_revisione"])
    exception_text = (
        "\n".join(f"- Topic {item['topic_id']}: {item['reason']}" for item in exceptions)
        if exceptions else "- Nessuna eccezione alla diversificazione per dominio."
    )
    return f"""# Guida allo human check dei topic

## Scopo

Il campione è selezionato automaticamente e in modo riproducibile. Il giudizio
semantico resta umano: non modificare le colonne di provenienza o selezione.

## Come è costruito il campione

- Topic utili `{config['topic_utili']}`: {config['top_weight_per_topic']} record ad alto peso e {config['random_per_topic']} casuali per topic.
- Topic di controllo artefatto `{config['topic_artefatto']}`: {config['artifact_checks_per_topic']} record ad alto peso per topic.
- Seed casuale: `{config['random_seed']}`.
- Massimo desiderato per dominio nei topic utili: `{config['max_same_domain_per_topic']}`.
- Duplicati esatti titolo + estratto esclusi.

## Categorie per `classificazione_umana`

{categories}

Per `boilerplate_si_no` e `duplicato_sospetto_si_no` usare: `sì`, `no`, `incerto`.
Per `decisione_inclusione` usare: `mantenere`, `escludere`, `riesaminare`.

Compilare anche `etichetta_tema_proposta` e `note_revisore` quando utili. La
`valutazione_preliminare` descrive soltanto il motivo automatico della selezione.

## Eccezioni documentate

{exception_text}

## Limiti

Il campione non stima la prevalenza dei temi e non misura stance, consenso o
comportamento politico. Serve esclusivamente a controllare interpretabilità,
boilerplate, contenuti non politici e casi dubbi.
"""


def build_selection_manifest(
    repo_root: Path,
    config: Mapping[str, Any],
    input_paths: Sequence[Path],
    sample: pd.DataFrame,
    exceptions: Sequence[Mapping[str, Any]],
    output_paths: Sequence[Path],
    run_time_utc: datetime | None = None,
) -> dict[str, Any]:
    """Costruisce il manifest con provenienza, regole, conteggi e hash."""

    timestamp = (run_time_utc or datetime.now(timezone.utc)).astimezone(timezone.utc).isoformat()
    counts_topic = sample["topic_id"].value_counts().sort_index()
    counts_type = sample["tipo_selezione"].value_counts().sort_index()
    manifest_path = f"{str(config['output_directory']).rstrip('/')}/selection_manifest.json"
    return {
        "run_at_utc": timestamp,
        "python_version": platform.python_version(),
        "pandas_version": pd.__version__,
        "inputs": [
            {"path": _relative(repo_root, path), "size_bytes": path.stat().st_size, "sha256": sha256_file(path)}
            for path in input_paths
        ],
        "configuration": dict(config),
        "random_seed": int(config["random_seed"]),
        "selection_rules": {
            "deduplication": "exact title + excerpt before selection",
            "top_weight_order": "descending topic-specific NMF weight, source_row_index tie-break",
            "random_order": "pandas sample without replacement, random_state = seed + topic_id",
            "domain_diversification": "prefer least-used domains, then document unavoidable exceptions",
        },
        "counts_by_topic": {str(key): int(value) for key, value in counts_topic.items()},
        "counts_by_selection_type": {str(key): int(value) for key, value in counts_type.items()},
        "domain_diversification_exceptions": list(exceptions),
        "personal_absolute_paths_present": False,
        "outputs": [
            {"path": _relative(repo_root, path), "size_bytes": path.stat().st_size, "sha256": sha256_file(path)}
            for path in output_paths
        ] + [{
            "path": manifest_path,
            "size_bytes": None,
            "sha256": None,
            "note": "Self-hash non incorporato per evitare ricorsione del contenuto.",
        }],
    }


def write_outputs(
    repo_root: Path,
    config: Mapping[str, Any],
    review_path: Path,
    terms_path: Path,
    result: SelectionResult,
    run_time_utc: datetime | None = None,
) -> dict[str, Path]:
    """Scrive campione, riepilogo, guida e manifest nella directory configurata."""

    output_dir = resolve_repo_path(repo_root, str(config["output_directory"]))
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "review_sample": output_dir / "review_sample.csv",
        "selection_summary": output_dir / "selection_summary.csv",
        "review_guide": output_dir / "review_guide.md",
        "selection_manifest": output_dir / "selection_manifest.json",
    }
    result.sample.to_csv(paths["review_sample"], index=False, encoding=str(config["encoding"]))
    summary = generate_selection_summary(result.sample, result.exceptions)
    summary.to_csv(paths["selection_summary"], index=False, encoding="utf-8")
    paths["review_guide"].write_text(generate_review_guide(config, result.exceptions), encoding="utf-8")
    hashed_outputs = [paths["review_sample"], paths["selection_summary"], paths["review_guide"]]
    manifest = build_selection_manifest(
        repo_root, config, [review_path, terms_path], result.sample,
        result.exceptions, hashed_outputs, run_time_utc,
    )
    paths["selection_manifest"].write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return paths


def run_human_review(repo_root: Path, config: Mapping[str, Any]) -> tuple[SelectionResult, dict[str, Path]]:
    """Carica, seleziona, valida e scrive gli output senza modificare gli input."""

    review_path = resolve_repo_path(repo_root, str(config["input_review_csv"]))
    terms_path = resolve_repo_path(repo_root, str(config["input_topic_terms_csv"]))
    review, _terms = load_inputs(review_path, terms_path, config)
    result = build_review_sample(review, config)
    paths = write_outputs(repo_root, config, review_path, terms_path, result)
    return result, paths
