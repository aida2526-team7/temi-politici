#!/bin/zsh
# Continua la pipeline dopo una discovery Media Cloud gia' avviata.
# Da eseguire in background con caffeinate: vedi il README o il notebook.

set -euo pipefail

ROOT="${0:A:h:h}"
PYTHON_BIN="${PYTHON_BIN:-python}"
URLS_FILE="$ROOT/data/raw/mediacloud_urls.jsonl"

log() {
  print -r -- "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

cd "$ROOT"
log "Pipeline notturna avviata. Python: $(command -v "$PYTHON_BIN")"

# Non leggere un JSONL mentre il processo di discovery lo sta ancora scrivendo.
while /usr/bin/pgrep -f 'mediacloud_spike\.py' >/dev/null; do
  log "Discovery ancora in corso: attendo 60 secondi."
  sleep 60
done

if [[ ! -s "$URLS_FILE" ]]; then
  log "ERRORE: manca o e' vuoto $URLS_FILE. Il full-text non viene avviato."
  exit 2
fi

log "Discovery conclusa. Avvio download full-text e pulizia."
"$PYTHON_BIN" src/mediacloud_fulltext.py

log "Full-text concluso. Avvio classificatore con 12 topic."
"$PYTHON_BIN" src/news_topic_model.py --n-topics 12

log "Pipeline notturna completata con successo."
