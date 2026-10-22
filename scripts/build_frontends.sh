#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
for app in frontend/app frontend/network-artifacts; do
  echo "==> Building $app"
  (
    cd "$ROOT/$app"
    if [[ -f package-lock.json ]]; then
      npm ci --no-audit --no-fund
    else
      npm install --no-audit --no-fund
    fi
    npm run build
  )
done
echo "Frontend builds completed."
