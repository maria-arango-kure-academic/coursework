#!/bin/bash
set -euo pipefail
umask 077
BASE=/srv/keeper/services/vfi-simulation
exec 9>"$BASE/update.lock"
flock -n 9 || exit 0
KEY=/root/.ssh/vfi_simulation_deploy
[ -f "$KEY" ] || exit 0
export GIT_TERMINAL_PROMPT=0
export GIT_SSH_COMMAND='ssh -i /root/.ssh/vfi_simulation_deploy -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=yes'
if [ ! -d "$BASE/repository/.git" ]; then
    git clone --branch main --single-branch git@github.com:maria-arango-kure-academic/vfi-simulation.git "$BASE/repository" || exit 1
fi
cd "$BASE/repository"
[ -z "$(git status --porcelain)" ] || { echo 'Checkout has local changes; update stopped.'; exit 1; }
git fetch --quiet origin main
TARGET=$(git rev-parse origin/main)
[ "$TARGET" != "$(cat "$BASE/published-commit" 2>/dev/null || true)" ] || exit 0
git merge --ff-only origin/main
RELEASE="$BASE/releases/$TARGET"
install -d "$RELEASE"
git archive "$TARGET" | tar -xf - -C "$RELEASE"
export VFI_ENV_FILE="$BASE/.env" VFI_DATA_DIR="$BASE/data"
export VFI_IMAGE="vfi-simulation:$TARGET"
OLD_RELEASE=$(readlink -f "$BASE/current")
OLD_IMAGE=$(cat "$BASE/current-image")
docker compose -p vfi-simulation -f "$RELEASE/compose.yaml" build
docker compose -p vfi-simulation -f "$RELEASE/compose.yaml" up -d --no-build
ID=$(docker compose -p vfi-simulation -f "$RELEASE/compose.yaml" ps -q simulation)
for attempt in $(seq 1 60); do
    if [ "$(docker inspect --format '{{.State.Health.Status}}' "$ID")" = healthy ]; then
        ln -sfn "$RELEASE" "$BASE/current"
        printf '%s\n' "$VFI_IMAGE" > "$BASE/current-image"
        printf '%s\n' "$TARGET" > "$BASE/published-commit"
        echo "$(date -Iseconds): published $TARGET"
        exit 0
    fi
    sleep 2
done
export VFI_IMAGE="$OLD_IMAGE"
docker compose -p vfi-simulation -f "$OLD_RELEASE/compose.yaml" up -d --no-build
echo "$(date -Iseconds): health check failed; restored previous application image."
exit 1
