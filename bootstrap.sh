#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-.}"
FORCE_FLAG="${2:-}"

COMMAND=(python3 "$ROOT_DIR/skills/design-token-context/scripts/scaffold_ai_context.py" --target "$TARGET")

if [[ "$FORCE_FLAG" == "--force" ]]; then
  COMMAND+=("--force")
fi

"${COMMAND[@]}"

echo
echo "Scaffolded .ai-context into: $TARGET"
