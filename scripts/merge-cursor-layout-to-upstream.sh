#!/usr/bin/env bash
# Merge cursor-layout cross-link into tsonmiramar/harness.
# Requires GitHub credentials for the tsonmiramar account (not sondo-appfolio).
set -euo pipefail

UPSTREAM_REPO="${UPSTREAM_REPO:-https://github.com/tsonmiramar/harness.git}"
SOURCE_REPO="${SOURCE_REPO:-https://github.com/sondo-appfolio/tsonmiramar-harness.git}"
SOURCE_REF="${SOURCE_REF:-main}"

WORKDIR="${WORKDIR:-$(mktemp -d)}"
trap 'rm -rf "$WORKDIR"' EXIT

git clone "$UPSTREAM_REPO" "$WORKDIR/upstream"
cd "$WORKDIR/upstream"

git remote add contrib "$SOURCE_REPO"
git fetch contrib "$SOURCE_REF"

git checkout main
git merge --no-ff "contrib/$SOURCE_REF" -m "$(cat <<'EOF'
feat(cursor): add Cursor runtime cross-link to meta-harness

Link sondo-appfolio/meta-harness as the Cursor layout port and document
the cross-runtime matrix alongside Claude Code and Codex.
EOF
)"

git push origin main

echo "Merged contrib/$SOURCE_REF into tsonmiramar/harness main."
