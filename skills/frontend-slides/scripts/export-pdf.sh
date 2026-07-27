#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -lt 1 ]; then
  echo "Usage: bash scripts/export-pdf.sh <presentation.html> [output.pdf]" >&2
  exit 1
fi
HTML_FILE="$1"
OUT_FILE="${2:-presentation.pdf}"
echo "Exporting $HTML_FILE to $OUT_FILE requires a local browser/PDF pipeline such as Playwright."
echo "In ChatGPT, create the HTML first, then export with your local tool of choice."
