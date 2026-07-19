param([string]$Agent = "codex")
$ErrorActionPreference = "Stop"
npx skills add Kvxw1105/kv-skills --skill '*' --agent $Agent --global --yes --full-depth
