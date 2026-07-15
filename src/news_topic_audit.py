"""Audit riproducibile degli output del classificatore NMF.

Il modulo separa calcolo, lettura/scrittura e presentazione. Non addestra modelli,
non modifica gli input e non assegna etichette semantiche ai topic.
"""

from __future__ import annotations

import hashlib
import json
import platform
import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


REQUIRED_BASE_COLUMNS = {
    "url",
    "domain",
    "seendate",
    "title",
    "language",
    "chars",
    "estratto",
    "topic_id",
    "confidenza_topic",
    "termini_caratteristici",
}
WEIGHT_COLUMN_PATTERN = re.compile(r"^topic_(\d+)_peso$")


@dataclass(frozen=True)
class AuditResults:
    """Risultati in memoria, indipendenti dalla serializzazione su disco."""

    topic_distribution: pd.DataFrame
    confidence_summary: pd.DataFrame
    domain_summary: pd.DataFrame
    temporal_summary: pd.DataFrame
    duplicate_summary: dict[str, Any]
    top_records: pd.DataFrame
    sampled_records: pd.DataFrame
    topic_terms: dict[int, str]
    metadata: dict[str, Any]
    warnings: tuple[str, ...]


def find_repo_root(start: Path | None = None) -> Path:
    """Individua la root cercando una directory `.git` nei genitori."""

    current = (start or Path.cwd()).resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    raise FileNotFoundError("Root Git non trovata a partire dal percorso indicato.")


def resolve_repo_path(repo_root: Path, relative_path: str) -> Path:
    """Risolve un percorso relativo impedendo uscite dalla root del repository."""

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
    """Carica e valida la configurazione JSON senza trasformare i percorsi in output."""

    config = json.loads(config_path.read_text(encoding="utf-8"))
    required = {
        "input_review_csv",
        "input_metadata_json",
        "output_dir",
        "random_seed",
        "near_duplicate_prefix_length",
        "confidence_thresholds",
        "top_domains",
        "top_records",
        "sample_records",
        "encoding",
    }
    missing = required - set(config)
    if missing:
        raise ValueError(f"Configurazione incompleta: {sorted(missing)}")
    for key in ("input_review_csv", "input_metadata_json", "output_dir"):
        resolve_repo_path(repo_root, str(config[key]))
    if int(config["near_duplicate_prefix_length"]) <= 0:
        raise ValueError("near_duplicate_prefix_length deve essere positivo")
    if any(not 0 < float(value) <= 1 for value in config["confidence_thresholds"]):
        raise ValueError("Le soglie di confidenza devono essere comprese tra 0 e 1")
    return config


def load_review_csv(path: Path, encoding: str = "utf-8-sig") -> pd.DataFrame:
    """Carica il CSV di review in modo esplicito e verifica subito lo schema."""

    if not path.is_file():
        raise FileNotFoundError(f"Review CSV non trovato: {path.name}")
    frame = pd.read_csv(path, encoding=encoding, low_memory=False)
    validate_required_columns(frame)
    return frame


def load_metadata_json(path: Path) -> dict[str, Any]:
    """Carica il metadata JSON e richiede un oggetto alla radice."""

    if not path.is_file():
        raise FileNotFoundError(f"Metadata JSON non trovato: {path.name}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Il metadata JSON deve contenere un oggetto")
    return value


def topic_weight_columns(frame: pd.DataFrame) -> list[str]:
    """Restituisce le colonne `topic_N_peso` ordinate per identificativo."""

    indexed: list[tuple[int, str]] = []
    for column in frame.columns:
        match = WEIGHT_COLUMN_PATTERN.match(str(column))
        if match:
            indexed.append((int(match.group(1)), str(column)))
    indexed.sort()
    return [column for _, column in indexed]


def validate_required_columns(frame: pd.DataFrame) -> list[str]:
    """Verifica colonne di base, almeno un peso e continuità degli identificativi."""

    missing = REQUIRED_BASE_COLUMNS - set(frame.columns)
    if missing:
        raise ValueError(f"Colonne obbligatorie mancanti: {sorted(missing)}")
    weights = topic_weight_columns(frame)
    if not weights:
        raise ValueError("Nessuna colonna topic_N_peso trovata")
    expected = [f"topic_{index}_peso" for index in range(len(weights))]
    if weights != expected:
        raise ValueError(f"Colonne dei pesi non continue: attese {expected}, trovate {weights}")
    return weights


def article_distribution(frame: pd.DataFrame) -> pd.DataFrame:
    """Conta gli articoli assegnati a ogni topic e calcola la quota percentuale."""

    total = len(frame)
    counts = frame["topic_id"].value_counts(dropna=False).sort_index()
    result = counts.rename("articles").reset_index().rename(columns={"index": "topic_id"})
    result["topic_id"] = result["topic_id"].astype(int)
    result["percentage"] = result["articles"] / total * 100 if total else 0.0
    return result


def _describe_series(variable: str, series: pd.Series) -> list[dict[str, Any]]:
    numeric = pd.to_numeric(series, errors="raise")
    quantiles = numeric.quantile([0.25, 0.50, 0.75, 0.90, 0.99])
    return [
        {"variable": variable, "metric": "min", "value": float(numeric.min())},
        {"variable": variable, "metric": "mean", "value": float(numeric.mean())},
        {"variable": variable, "metric": "median", "value": float(quantiles.loc[0.50])},
        {"variable": variable, "metric": "p25", "value": float(quantiles.loc[0.25])},
        {"variable": variable, "metric": "p75", "value": float(quantiles.loc[0.75])},
        {"variable": variable, "metric": "p90", "value": float(quantiles.loc[0.90])},
        {"variable": variable, "metric": "p99", "value": float(quantiles.loc[0.99])},
        {"variable": variable, "metric": "exactly_1_percentage", "value": float(numeric.eq(1.0).mean() * 100)},
    ]


def confidence_statistics(frame: pd.DataFrame, thresholds: Sequence[float]) -> pd.DataFrame:
    """Calcola statistiche descrittive e quote sotto soglie esplicite."""

    rows = _describe_series("confidenza_topic", frame["confidenza_topic"])
    numeric = pd.to_numeric(frame["confidenza_topic"], errors="raise")
    for threshold in thresholds:
        rows.append(
            {
                "variable": "confidenza_topic",
                "metric": f"below_{float(threshold):.2f}_percentage",
                "value": float(numeric.lt(float(threshold)).mean() * 100),
            }
        )
    return pd.DataFrame(rows)


def topic_weight_statistics(frame: pd.DataFrame) -> pd.DataFrame:
    """Calcola le stesse statistiche per ogni peso NMF."""

    rows: list[dict[str, Any]] = []
    for column in validate_required_columns(frame):
        rows.extend(_describe_series(column, frame[column]))
    return pd.DataFrame(rows)


def prevalent_domains(frame: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Conta e ordina i domini per topic, includendo quota e rango."""

    working = frame[["topic_id", "domain"]].copy()
    working["domain"] = working["domain"].fillna("[MISSING]")
    counts = working.groupby(["topic_id", "domain"], dropna=False).size().rename("articles").reset_index()
    totals = working.groupby("topic_id").size().rename("topic_articles")
    counts = counts.merge(totals, on="topic_id", how="left")
    counts["topic_percentage"] = counts["articles"] / counts["topic_articles"] * 100
    counts = counts.sort_values(["topic_id", "articles", "domain"], ascending=[True, False, True])
    counts["rank"] = counts.groupby("topic_id").cumcount() + 1
    return counts[counts["rank"] <= int(top_n)].reset_index(drop=True)


def dominant_domain_share(frame: pd.DataFrame) -> pd.DataFrame:
    """Restituisce il primo dominio e la relativa quota per ogni topic."""

    domains = prevalent_domains(frame, top_n=1)
    return domains[["topic_id", "domain", "articles", "topic_articles", "topic_percentage"]].copy()


def temporal_distribution(frame: pd.DataFrame) -> pd.DataFrame:
    """Conta gli articoli per topic e mese, senza modificare il DataFrame."""

    dates = pd.to_datetime(frame["seendate"], errors="coerce")
    working = pd.DataFrame({"topic_id": frame["topic_id"].to_numpy(), "date": dates})
    working["year_month"] = working["date"].dt.to_period("M").astype("string")
    result = (
        working.dropna(subset=["year_month"])
        .groupby(["topic_id", "year_month"])
        .size()
        .rename("articles")
        .reset_index()
    )
    return result


def exact_excerpt_duplicates(frame: pd.DataFrame) -> dict[str, int]:
    """Quantifica gruppi e record con estratto esattamente identico."""

    values = frame["estratto"].fillna("").astype(str)
    counts = values[values.ne("")].value_counts()
    repeated = counts[counts > 1]
    return {
        "records_in_duplicate_groups": int(repeated.sum()),
        "duplicate_groups": int(len(repeated)),
        "largest_group": int(repeated.max()) if len(repeated) else 0,
    }


def exact_title_excerpt_duplicates(frame: pd.DataFrame) -> dict[str, int]:
    """Quantifica duplicati della coppia titolo più estratto."""

    working = frame[["title", "estratto"]].fillna("").astype(str)
    valid = working["title"].ne("") | working["estratto"].ne("")
    counts = working[valid].value_counts()
    repeated = counts[counts > 1]
    return {
        "records_in_duplicate_groups": int(repeated.sum()),
        "duplicate_groups": int(len(repeated)),
        "largest_group": int(repeated.max()) if len(repeated) else 0,
    }


def normalize_excerpt(value: Any) -> str:
    """Normalizza un estratto per il proxy lessicale dei quasi duplicati."""

    text = str(value or "").lower()
    text = re.sub(r"[^a-zàèéìòóù0-9 ]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def near_duplicate_proxy(frame: pd.DataFrame, prefix_length: int) -> dict[str, int | str]:
    """Raggruppa estratti con lo stesso prefisso normalizzato di lunghezza data."""

    prefixes = frame["estratto"].fillna("").map(normalize_excerpt).str[: int(prefix_length)]
    counts = prefixes[prefixes.ne("")].value_counts()
    repeated = counts[counts > 1]
    return {
        "prefix_length": int(prefix_length),
        "records_in_duplicate_groups": int(repeated.sum()),
        "duplicate_groups": int(len(repeated)),
        "largest_group": int(repeated.max()) if len(repeated) else 0,
        "definition": "same normalized prefix of the review excerpt",
    }


def _has_non_latin_letter(value: Any) -> bool:
    for character in str(value or ""):
        if character.isalpha() and ord(character) > 127:
            if "LATIN" not in unicodedata.name(character, ""):
                return True
    return False


def quantitative_anomalies(frame: pd.DataFrame) -> dict[str, Any]:
    """Calcola anomalie osservabili senza attribuire significato semantico."""

    excerpt_counts = frame["estratto"].fillna("").astype(str).value_counts()
    largest_excerpt = excerpt_counts.index[0] if len(excerpt_counts) else ""
    largest_mask = frame["estratto"].fillna("").astype(str).eq(largest_excerpt)
    largest_topics = (
        frame.loc[largest_mask, "topic_id"].value_counts().sort_index().astype(int).to_dict()
        if largest_excerpt
        else {}
    )
    non_latin = frame["title"].map(_has_non_latin_letter)
    language_it = frame["language"].eq("it")
    return {
        "rows": int(len(frame)),
        "duplicate_url_records": int(frame["url"].duplicated(keep=False).sum()),
        "largest_exact_excerpt_group": int(excerpt_counts.iloc[0]) if len(excerpt_counts) else 0,
        "largest_exact_excerpt_topic_distribution": {str(key): int(value) for key, value in largest_topics.items()},
        "non_latin_title_language_it_records": int((non_latin & language_it).sum()),
    }


def select_top_records(frame: pd.DataFrame, records_per_topic: int) -> pd.DataFrame:
    """Seleziona deterministicamente i record col peso specifico più alto."""

    weights = validate_required_columns(frame)
    selected: list[pd.DataFrame] = []
    for topic_id, group in frame.groupby("topic_id", sort=True):
        topic_index = int(topic_id)
        column = f"topic_{topic_index}_peso"
        if column not in weights:
            raise ValueError(f"Peso mancante per topic {topic_index}")
        ordered = group.sort_values([column, "url"], ascending=[False, True]).head(int(records_per_topic)).copy()
        ordered["selection_rank"] = range(1, len(ordered) + 1)
        ordered["selected_weight"] = ordered[column]
        selected.append(ordered)
    return pd.concat(selected, ignore_index=True) if selected else pd.DataFrame()


def sample_assigned_records(frame: pd.DataFrame, records_per_topic: int, seed: int) -> pd.DataFrame:
    """Campiona record per topic con seed deterministico e senza replacement."""

    selected: list[pd.DataFrame] = []
    for topic_id, group in frame.groupby("topic_id", sort=True):
        size = min(int(records_per_topic), len(group))
        sample = group.sample(n=size, random_state=int(seed) + int(topic_id), replace=False).copy()
        sample = sample.sort_values("url").reset_index(drop=True)
        sample["selection_rank"] = range(1, len(sample) + 1)
        sample["selected_weight"] = sample[f"topic_{int(topic_id)}_peso"]
        selected.append(sample)
    return pd.concat(selected, ignore_index=True) if selected else pd.DataFrame()


def build_audit_results(frame: pd.DataFrame, metadata: Mapping[str, Any], config: Mapping[str, Any]) -> AuditResults:
    """Esegue tutti i calcoli puri dell'audit senza scrivere su disco."""

    validate_required_columns(frame)
    distribution = article_distribution(frame)
    confidence = pd.concat(
        [confidence_statistics(frame, config["confidence_thresholds"]), topic_weight_statistics(frame)],
        ignore_index=True,
    )
    domains = prevalent_domains(frame, int(config["top_domains"]))
    temporal = temporal_distribution(frame)
    exact_excerpt = exact_excerpt_duplicates(frame)
    exact_pair = exact_title_excerpt_duplicates(frame)
    near = near_duplicate_proxy(frame, int(config["near_duplicate_prefix_length"]))
    anomalies = quantitative_anomalies(frame)
    duplicate_summary = {
        "exact_excerpt": exact_excerpt,
        "exact_title_excerpt": exact_pair,
        "near_duplicate_proxy": near,
        "anomalies": anomalies,
    }
    top = select_top_records(frame, int(config["top_records"]))
    sampled = sample_assigned_records(frame, int(config["sample_records"]), int(config["random_seed"]))
    terms = (
        frame[["topic_id", "termini_caratteristici"]]
        .drop_duplicates("topic_id")
        .set_index("topic_id")["termini_caratteristici"]
        .astype(str)
        .to_dict()
    )
    warnings: list[str] = []
    metadata_input = str(metadata.get("input", ""))
    if metadata_input and Path(metadata_input).is_absolute():
        warnings.append("Il metadata sorgente contiene un percorso input assoluto; il percorso è oscurato negli output.")
    threshold = float(config.get("dominant_domain_warning_threshold", 0.5)) * 100
    dominant = domains[domains["rank"] == 1]
    concentrated = dominant.loc[dominant["topic_percentage"] >= threshold, "topic_id"].astype(int).tolist()
    if concentrated:
        warnings.append(f"Topic con dominio dominante >= {threshold:.1f}%: {concentrated}")
    return AuditResults(
        topic_distribution=distribution,
        confidence_summary=confidence,
        domain_summary=domains,
        temporal_summary=temporal,
        duplicate_summary=duplicate_summary,
        top_records=top,
        sampled_records=sampled,
        topic_terms={int(key): value for key, value in terms.items()},
        metadata=dict(metadata),
        warnings=tuple(warnings),
    )


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Calcola SHA-256 con lettura streaming."""

    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def _relative(repo_root: Path, path: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def _markdown_table(headers: Sequence[str], rows: Iterable[Sequence[Any]]) -> str:
    def clean(value: Any) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    output = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    output.extend("| " + " | ".join(clean(value) for value in row) + " |" for row in rows)
    return "\n".join(output)


def _sanitized_metadata(metadata: Mapping[str, Any]) -> dict[str, Any]:
    sanitized = dict(metadata)
    if "input" in sanitized:
        sanitized["input"] = Path(str(sanitized["input"])).name
    return sanitized


def generate_markdown_report(results: AuditResults, config: Mapping[str, Any]) -> str:
    """Genera il report Markdown esclusivamente dai risultati calcolati."""

    distribution_rows = [
        (int(row.topic_id), int(row.articles), f"{row.percentage:.3f}%")
        for row in results.topic_distribution.itertuples(index=False)
    ]
    confidence = results.confidence_summary
    confidence_only = confidence[confidence["variable"] == "confidenza_topic"]
    confidence_rows = [(row.metric, f"{row.value:.8f}") for row in confidence_only.itertuples(index=False)]
    duplicate_rows = []
    for section in ("exact_excerpt", "exact_title_excerpt", "near_duplicate_proxy"):
        for metric, value in results.duplicate_summary[section].items():
            duplicate_rows.append((section, metric, value))

    lines = [
        "# Audit riproducibile degli output NMF",
        "",
        "> Report generato automaticamente da `scripts/run_topic_audit.py`.",
        "",
        "## Fatti quantitativi",
        "",
        "### Distribuzione dei topic",
        "",
        _markdown_table(["Topic", "Articoli", "Percentuale"], distribution_rows),
        "",
        "Output tabellare: [`topic_distribution.csv`](topic_distribution.csv).",
        "",
        "### Confidenza normalizzata",
        "",
        _markdown_table(["Metrica", "Valore"], confidence_rows),
        "",
        "La confidenza è `max(pesi NMF) / somma(pesi NMF)`: non è una probabilità calibrata.",
        "Output completo: [`confidence_summary.csv`](confidence_summary.csv).",
        "",
        "### Duplicazioni",
        "",
        _markdown_table(["Sezione", "Metrica", "Valore"], duplicate_rows),
        "",
        "Output strutturato: [`duplicate_summary.json`](duplicate_summary.json).",
        "",
        "### Parametri registrati dal classificatore",
        "",
        "```json",
        json.dumps(_sanitized_metadata(results.metadata), ensure_ascii=False, indent=2),
        "```",
        "",
        "## Evidenze per topic",
        "",
    ]
    for distribution_row in results.topic_distribution.itertuples(index=False):
        topic_id = int(distribution_row.topic_id)
        domains = results.domain_summary[results.domain_summary["topic_id"] == topic_id]
        months = results.temporal_summary[results.temporal_summary["topic_id"] == topic_id]
        top = results.top_records[results.top_records["topic_id"] == topic_id]
        sample = results.sampled_records[results.sampled_records["topic_id"] == topic_id]
        lines.extend(
            [
                f"### Topic {topic_id}",
                "",
                f"- Articoli: {int(distribution_row.articles)} ({distribution_row.percentage:.3f}%).",
                f"- Termini registrati: {results.topic_terms.get(topic_id, '')}",
                "- Interpretazione semantica: **da validare da una persona**.",
                "",
                "Domini prevalenti:",
                "",
                _markdown_table(
                    ["Rank", "Dominio", "Articoli", "% topic"],
                    [
                        (int(row.rank), row.domain, int(row.articles), f"{row.topic_percentage:.3f}%")
                        for row in domains.itertuples(index=False)
                    ],
                ),
                "",
                "Distribuzione mensile:",
                "",
                _markdown_table(
                    ["Mese", "Articoli"],
                    [(row.year_month, int(row.articles)) for row in months.itertuples(index=False)],
                ),
                "",
                "Record con peso più alto:",
                "",
                _markdown_table(
                    ["Rank", "Peso", "Dominio", "Data", "Titolo"],
                    [
                        (int(row.selection_rank), f"{row.selected_weight:.8f}", row.domain, row.seendate, str(row.title)[:180])
                        for row in top.itertuples(index=False)
                    ],
                ),
                "",
                f"Campione deterministico, seed base {int(config['random_seed'])}:",
                "",
                _markdown_table(
                    ["Rank", "Peso", "Confidenza", "Dominio", "Data", "Titolo"],
                    [
                        (
                            int(row.selection_rank),
                            f"{row.selected_weight:.8f}",
                            f"{row.confidenza_topic:.8f}",
                            row.domain,
                            row.seendate,
                            str(row.title)[:180],
                        )
                        for row in sample.itertuples(index=False)
                    ],
                ),
                "",
            ]
        )
    lines.extend(
        [
            "## Interpretazioni e limiti",
            "",
            "- I conteggi precedenti sono fatti quantitativi riproducibili.",
            "- Il report non assegna nomi definitivi né giudizi semantici ai topic.",
            "- I quasi duplicati sono un proxy basato sul prefisso normalizzato degli estratti, non sul full-text.",
            "- Gli estratti hanno lunghezza massima di 500 caratteri.",
            "- I record ad alto peso possono rappresentare boilerplate molto distintivo.",
            "",
            "## Avvisi automatici",
            "",
        ]
    )
    lines.extend([f"- {warning}" for warning in results.warnings] or ["- Nessun avviso."])
    lines.extend(
        [
            "",
            "## Output",
            "",
            "- [`topic_distribution.csv`](topic_distribution.csv)",
            "- [`confidence_summary.csv`](confidence_summary.csv)",
            "- [`domain_summary.csv`](domain_summary.csv)",
            "- [`duplicate_summary.json`](duplicate_summary.json)",
            "- [`run_manifest.json`](run_manifest.json)",
            "",
        ]
    )
    return "\n".join(lines)


def generate_tabular_outputs(results: AuditResults, output_dir: Path) -> dict[str, Path]:
    """Scrive le tabelle e il JSON dei duplicati nella directory autorizzata."""

    output_dir.mkdir(parents=True, exist_ok=True)
    distribution = results.topic_distribution.copy()
    date_ranges = (
        results.temporal_summary.groupby("topic_id")["year_month"]
        .agg(date_min="min", date_max="max")
        .reset_index()
    )
    monthly = (
        results.temporal_summary.groupby("topic_id")
        .apply(lambda group: json.dumps(dict(zip(group["year_month"], group["articles"].astype(int))), ensure_ascii=False), include_groups=False)
        .rename("monthly_distribution")
        .reset_index()
    )
    distribution = distribution.merge(date_ranges, on="topic_id", how="left").merge(monthly, on="topic_id", how="left")
    paths = {
        "topic_distribution": output_dir / "topic_distribution.csv",
        "confidence_summary": output_dir / "confidence_summary.csv",
        "domain_summary": output_dir / "domain_summary.csv",
        "duplicate_summary": output_dir / "duplicate_summary.json",
    }
    distribution.to_csv(paths["topic_distribution"], index=False, encoding="utf-8")
    results.confidence_summary.to_csv(paths["confidence_summary"], index=False, encoding="utf-8")
    results.domain_summary.to_csv(paths["domain_summary"], index=False, encoding="utf-8")
    paths["duplicate_summary"].write_text(
        json.dumps(results.duplicate_summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return paths


def build_run_manifest(
    repo_root: Path,
    config: Mapping[str, Any],
    input_paths: Sequence[Path],
    review_frame: pd.DataFrame,
    output_paths: Sequence[Path],
    warnings: Sequence[str],
    run_time_utc: datetime | None = None,
) -> dict[str, Any]:
    """Costruisce un manifest senza percorsi assoluti personali."""

    try:
        import sklearn

        sklearn_version: str | None = sklearn.__version__
    except ImportError:
        sklearn_version = None
    timestamp = (run_time_utc or datetime.now(timezone.utc)).astimezone(timezone.utc).isoformat()
    inputs = [
        {
            "path": _relative(repo_root, path),
            "size_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for path in input_paths
    ]
    outputs = [
        {
            "path": _relative(repo_root, path),
            "size_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for path in output_paths
    ]
    outputs.append(
        {
            "path": f"{str(config['output_dir']).rstrip('/')}/run_manifest.json",
            "size_bytes": None,
            "sha256": None,
            "note": "Self-hash non incorporato per evitare ricorsione del contenuto.",
        }
    )
    return {
        "run_at_utc": timestamp,
        "python_version": platform.python_version(),
        "pandas_version": pd.__version__,
        "scikit_learn_version": sklearn_version,
        "inputs": inputs,
        "review_rows": int(len(review_frame)),
        "review_columns": [str(column) for column in review_frame.columns],
        "parameters": dict(config),
        "random_seed": int(config["random_seed"]),
        "outputs": outputs,
        "warnings": list(warnings) + ["Il manifest non incorpora il proprio hash SHA-256."],
    }


def write_audit_outputs(
    repo_root: Path,
    config: Mapping[str, Any],
    review_frame: pd.DataFrame,
    results: AuditResults,
    input_paths: Sequence[Path],
    run_time_utc: datetime | None = None,
) -> dict[str, Path]:
    """Serializza output, report e manifest dopo che i calcoli sono conclusi."""

    output_dir = resolve_repo_path(repo_root, str(config["output_dir"]))
    paths = generate_tabular_outputs(results, output_dir)
    report_path = output_dir / "audit_report.md"
    report_path.write_text(generate_markdown_report(results, config), encoding="utf-8")
    manifest_inputs = list(paths.values()) + [report_path]
    manifest = build_run_manifest(
        repo_root=repo_root,
        config=config,
        input_paths=input_paths,
        review_frame=review_frame,
        output_paths=manifest_inputs,
        warnings=results.warnings,
        run_time_utc=run_time_utc,
    )
    manifest_path = output_dir / "run_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    paths.update({"audit_report": report_path, "run_manifest": manifest_path})
    return paths


def run_audit(repo_root: Path, config: Mapping[str, Any]) -> tuple[AuditResults, dict[str, Path]]:
    """Carica input, calcola l'audit e scrive gli output autorizzati."""

    review_path = resolve_repo_path(repo_root, str(config["input_review_csv"]))
    metadata_path = resolve_repo_path(repo_root, str(config["input_metadata_json"]))
    review = load_review_csv(review_path, str(config["encoding"]))
    metadata = load_metadata_json(metadata_path)
    results = build_audit_results(review, metadata, config)
    paths = write_audit_outputs(repo_root, config, review, results, [review_path, metadata_path])
    return results, paths
