#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -lt 1 ]; then
  echo "Usage: bash scripts/deploy.sh <presentation.html-or-folder>" >&2
  exit 1
fi
echo "Deploy $1 with Vercel, Netlify, GitHub Pages, or another static host."
echo "For Vercel locally: npm i -g vercel && vercel --prod"
