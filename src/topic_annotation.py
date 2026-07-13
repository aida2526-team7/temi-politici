"""Preparazione e validazione auditabile delle annotazioni umane dei topic."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ANNOTATION_METADATA_COLUMNS = ["reviewer_id", "protocol_version", "fase_revisione"]
REQUIRED_COMPLETION_COLUMNS = [
    "classificazione_umana",
    "boilerplate_si_no",
    "duplicato_sospetto_si_no",
    "decisione_inclusione",
]


def find_repo_root(start: Path | None = None) -> Path:
    """Trova la root Git a partire da un file o una directory."""

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
    """Carica e valida configurazione, colonne, revisori e valori ammessi."""

    config = json.loads(config_path.read_text(encoding="utf-8"))
    required = {
        "input_sample", "input_manifest", "output_directory", "protocol_version",
        "reviewer_ids", "calibration_rows", "categorie_classificazione",
        "valori_booleani_ammessi", "decisioni_inclusione_ammesse", "encoding",
        "colonne_sorgente_immutabili", "colonne_compilabili",
    }
    missing = required - set(config)
    if missing:
        raise ValueError(f"Configurazione incompleta: {sorted(missing)}")
    for key in ("input_sample", "input_manifest", "output_directory"):
        resolve_repo_path(repo_root, str(config[key]))
    reviewer_ids = [str(value) for value in config["reviewer_ids"]]
    if len(reviewer_ids) != 2 or len(set(reviewer_ids)) != 2:
        raise ValueError("Servono esattamente due reviewer_id distinti")
    if str(config["protocol_version"]).strip() == "":
        raise ValueError("protocol_version non può essere vuota")
    if int(config["calibration_rows"]) <= 0:
        raise ValueError("calibration_rows deve essere positivo")
    immutable = list(map(str, config["colonne_sorgente_immutabili"]))
    fillable = list(map(str, config["colonne_compilabili"]))
    if "review_id" not in immutable:
        raise ValueError("review_id deve essere una colonna sorgente immutabile")
    if set(immutable) & set(fillable):
        raise ValueError("Colonne immutabili e compilabili devono essere disgiunte")
    return config


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Calcola SHA-256 con lettura streaming, senza modificare il file."""

    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def expected_sample_hash(manifest_path: Path, sample_relative_path: str) -> str:
    """Legge dal manifest l'hash atteso del campione sorgente."""

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    matches = [item for item in manifest.get("outputs", []) if item.get("path") == sample_relative_path]
    if len(matches) != 1 or not matches[0].get("sha256"):
        raise ValueError(f"Hash del campione non trovato nel manifest: {sample_relative_path}")
    return str(matches[0]["sha256"])


def verify_source_hash(sample_path: Path, manifest_path: Path, sample_relative_path: str) -> str:
    """Confronta hash corrente e registrato, interrompendo in caso di differenza."""

    expected = expected_sample_hash(manifest_path, sample_relative_path)
    actual = sha256_file(sample_path)
    if actual != expected:
        raise ValueError(f"Hash campione non coincidente: atteso {expected}, trovato {actual}")
    return actual


def read_csv_exact(path: Path, encoding: str) -> pd.DataFrame:
    """Legge ogni colonna come stringa preservando celle vuote e valori testuali."""

    if not path.is_file():
        raise FileNotFoundError(f"CSV non trovato: {path.name}")
    return pd.read_csv(path, encoding=encoding, dtype=str, keep_default_na=False)


def immutable_source_columns(config: Mapping[str, Any]) -> list[str]:
    """Restituisce in ordine le colonne che i revisori non possono modificare."""

    return [str(value) for value in config["colonne_sorgente_immutabili"]]


def validate_source_sample(sample: pd.DataFrame, config: Mapping[str, Any]) -> None:
    """Verifica schema, review_id, righe e stato vuoto delle colonne umane."""

    immutable = immutable_source_columns(config)
    fillable = [str(value) for value in config["colonne_compilabili"]]
    missing = set(immutable + fillable) - set(sample.columns)
    if missing:
        raise ValueError(f"Colonne mancanti nel campione: {sorted(missing)}")
    if sample.empty:
        raise ValueError("Il campione sorgente è vuoto")
    if sample["review_id"].eq("").any() or sample["review_id"].duplicated().any():
        raise ValueError("review_id vuoti o duplicati nel campione")
    nonempty = [column for column in fillable if sample[column].ne("").any()]
    if nonempty:
        raise ValueError(f"Il campione sorgente contiene già annotazioni: {nonempty}")
    if int(config["calibration_rows"]) >= len(sample):
        raise ValueError("calibration_rows deve essere inferiore al numero di record")


def create_reviewer_frame(
    sample: pd.DataFrame,
    reviewer_id: str,
    config: Mapping[str, Any],
) -> pd.DataFrame:
    """Crea un file revisore senza precompilare alcun giudizio semantico."""

    validate_source_sample(sample, config)
    immutable = immutable_source_columns(config)
    fillable = [str(value) for value in config["colonne_compilabili"]]
    frame = sample[immutable].copy()
    frame["reviewer_id"] = str(reviewer_id)
    frame["protocol_version"] = str(config["protocol_version"])
    calibration_rows = int(config["calibration_rows"])
    frame["fase_revisione"] = [
        "calibrazione" if index < calibration_rows else "indipendente"
        for index in range(len(frame))
    ]
    for column in fillable:
        frame[column] = ""
    return frame[immutable + ANNOTATION_METADATA_COLUMNS + fillable]


def create_reviewer_files(sample: pd.DataFrame, config: Mapping[str, Any]) -> dict[str, pd.DataFrame]:
    """Genera in memoria i due DataFrame nello stesso ordine del campione."""

    return {
        str(reviewer_id): create_reviewer_frame(sample, str(reviewer_id), config)
        for reviewer_id in config["reviewer_ids"]
    }


def validate_allowed_values(frame: pd.DataFrame, config: Mapping[str, Any]) -> None:
    """Rifiuta valori non vuoti che non appartengono ai vocabolari ammessi."""

    allowed = {
        "classificazione_umana": set(map(str, config["categorie_classificazione"])),
        "boilerplate_si_no": set(map(str, config["valori_booleani_ammessi"])),
        "duplicato_sospetto_si_no": set(map(str, config["valori_booleani_ammessi"])),
        "decisione_inclusione": set(map(str, config["decisioni_inclusione_ammesse"])),
    }
    for column, values in allowed.items():
        invalid = sorted(set(frame.loc[frame[column].ne(""), column]) - values)
        if invalid:
            raise ValueError(f"Valori non ammessi in {column}: {invalid}")


def verify_source_unchanged(
    annotation: pd.DataFrame,
    sample: pd.DataFrame,
    config: Mapping[str, Any],
) -> None:
    """Confronta ordine, review_id e ogni valore delle colonne immutabili."""

    immutable = immutable_source_columns(config)
    if len(annotation) != len(sample):
        raise ValueError(f"Numero righe modificato: {len(annotation)}, attese {len(sample)}")
    missing = set(immutable) - set(annotation.columns)
    if missing:
        raise ValueError(f"Colonne sorgente mancanti: {sorted(missing)}")
    for column in immutable:
        changed = annotation[column].reset_index(drop=True).ne(sample[column].reset_index(drop=True))
        if changed.any():
            rows = changed[changed].index.tolist()[:5]
            raise ValueError(f"Colonna sorgente modificata: {column}; righe {rows}")


def validate_identity_and_protocol(
    frame: pd.DataFrame,
    expected_reviewer_id: str,
    config: Mapping[str, Any],
) -> None:
    """Verifica reviewer_id, versione e assegnazione calibrazione/indipendente."""

    missing = set(ANNOTATION_METADATA_COLUMNS) - set(frame.columns)
    if missing:
        raise ValueError(f"Colonne protocollo mancanti: {sorted(missing)}")
    if not frame["reviewer_id"].eq(expected_reviewer_id).all():
        raise ValueError(f"reviewer_id non coerente con {expected_reviewer_id}")
    if not frame["protocol_version"].eq(str(config["protocol_version"])).all():
        raise ValueError("protocol_version mancante o modificata")
    calibration_rows = int(config["calibration_rows"])
    expected_phases = pd.Series(
        ["calibrazione" if index < calibration_rows else "indipendente" for index in range(len(frame))],
        dtype=str,
    )
    if not frame["fase_revisione"].reset_index(drop=True).eq(expected_phases).all():
        raise ValueError("fase_revisione modificata o non coerente")


def validate_annotation_completeness(frame: pd.DataFrame) -> None:
    """Richiede i quattro giudizi minimi per ogni record dopo la revisione."""

    incomplete = {
        column: int(frame[column].eq("").sum())
        for column in REQUIRED_COMPLETION_COLUMNS
        if frame[column].eq("").any()
    }
    if incomplete:
        raise ValueError(f"Annotazioni incomplete: {incomplete}")


def validate_annotation_frame(
    annotation: pd.DataFrame,
    sample: pd.DataFrame,
    expected_reviewer_id: str,
    config: Mapping[str, Any],
    require_complete: bool = True,
) -> None:
    """Esegue tutti i controlli senza modificare il DataFrame annotato."""

    fillable = [str(value) for value in config["colonne_compilabili"]]
    missing = set(fillable) - set(annotation.columns)
    if missing:
        raise ValueError(f"Colonne compilabili mancanti: {sorted(missing)}")
    verify_source_unchanged(annotation, sample, config)
    validate_identity_and_protocol(annotation, expected_reviewer_id, config)
    validate_allowed_values(annotation, config)
    if require_complete:
        validate_annotation_completeness(annotation)


def prepare_annotation_files(
    repo_root: Path,
    config: Mapping[str, Any],
) -> tuple[dict[str, Path], str]:
    """Verifica hash, genera e scrive i due file revisore senza toccare l'input."""

    sample_path = resolve_repo_path(repo_root, str(config["input_sample"]))
    manifest_path = resolve_repo_path(repo_root, str(config["input_manifest"]))
    source_hash = verify_source_hash(sample_path, manifest_path, str(config["input_sample"]))
    sample = read_csv_exact(sample_path, str(config["encoding"]))
    frames = create_reviewer_files(sample, config)
    output_dir = resolve_repo_path(repo_root, str(config["output_directory"]))
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}
    for reviewer_id, frame in frames.items():
        path = output_dir / f"reviewer_{reviewer_id}.csv"
        frame.to_csv(path, index=False, encoding=str(config["encoding"]))
        paths[reviewer_id] = path
    return paths, source_hash


def validate_annotation_files(
    repo_root: Path,
    config: Mapping[str, Any],
    require_complete: bool = True,
) -> dict[str, dict[str, int]]:
    """Valida i file su disco in sola lettura rispetto al campione originale."""

    sample_path = resolve_repo_path(repo_root, str(config["input_sample"]))
    manifest_path = resolve_repo_path(repo_root, str(config["input_manifest"]))
    verify_source_hash(sample_path, manifest_path, str(config["input_sample"]))
    sample = read_csv_exact(sample_path, str(config["encoding"]))
    output_dir = resolve_repo_path(repo_root, str(config["output_directory"]))
    counts: dict[str, dict[str, int]] = {}
    for reviewer_id in map(str, config["reviewer_ids"]):
        annotation = read_csv_exact(output_dir / f"reviewer_{reviewer_id}.csv", str(config["encoding"]))
        validate_annotation_frame(annotation, sample, reviewer_id, config, require_complete)
        fillable = [str(value) for value in config["colonne_compilabili"]]
        counts[reviewer_id] = {
            "rows": len(annotation),
            "calibration": int(annotation["fase_revisione"].eq("calibrazione").sum()),
            "independent": int(annotation["fase_revisione"].eq("indipendente").sum()),
            "filled_human_cells": int(annotation[fillable].ne("").sum().sum()),
        }
    return counts
