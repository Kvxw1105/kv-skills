#!/usr/bin/env bash
set -euo pipefail
agent="${1:-codex}"
npx skills add Kvxw1105/kv-skills --skill '*' --agent "$agent" --global --yes --full-depth
