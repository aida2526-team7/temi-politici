"""Mirror esplicito degli output della pipeline in una cartella Google Drive locale.

Google Drive Desktop espone una normale cartella locale: non servono API, token o
segreti nel repository. Il percorso e' configurato dall'utente, per non legare il
codice a un singolo account o computer.

Esempio:
    export GOOGLE_DRIVE_EXPORT_DIR="/percorso/alla/cartella/Politica Felice"
"""

import os
import shutil
from pathlib import Path


DRIVE_DIR_ENV = "GOOGLE_DRIVE_EXPORT_DIR"
LOCAL_CONFIG = Path(__file__).resolve().parents[1] / ".drive-export-dir"


def configured_drive_root():
    """Return the configured Drive root from the environment or local config.

    ``.drive-export-dir`` is deliberately ignored by Git: it may contain an
    account-specific macOS path and must never be shared with the repository.
    Only the terminating newline is removed, so valid spaces in a folder name
    are preserved.
    """
    from_environment = os.environ.get(DRIVE_DIR_ENV)
    if from_environment:
        return from_environment
    if LOCAL_CONFIG.is_file():
        return LOCAL_CONFIG.read_text(encoding="utf-8").removesuffix("\n").removesuffix("\r")
    return None


def mirror_file(source, section):
    """Copia ``source`` in ``$GOOGLE_DRIVE_EXPORT_DIR/<section>/``.

    La copia avviene prima in un file temporaneo e poi con una sostituzione atomica:
    Drive Desktop non deve quindi sincronizzare un JSONL o CSV a meta'. Se la
    variabile non e' impostata, la pipeline continua normalmente e stampa un avviso.
    Se e' impostata ma la copia fallisce, solleva l'errore: l'output locale resta
    comunque salvo e non viene dichiarato un deposito Drive inesistente.
    """
    destination_root = configured_drive_root()
    if not destination_root:
        print(f"Drive mirror skipped: set {DRIVE_DIR_ENV} or create {LOCAL_CONFIG.name}.")
        return None

    source = Path(source)
    if not source.is_file():
        raise FileNotFoundError(f"Cannot mirror missing file: {source}")

    destination = Path(destination_root).expanduser() / section / source.name
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".uploading")
    shutil.copy2(source, temporary)
    temporary.replace(destination)
    print(f"Drive mirror: {destination}")
    return destination
