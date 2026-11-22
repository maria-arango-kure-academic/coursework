#!/bin/bash
set -euo pipefail
umask 077
BASE=/srv/keeper/services/vfi-simulation
HOST=vfi.coursework.live
SITE=/etc/nginx/sites-available/vfi.coursework.live.conf
[ "$(id -u)" = 0 ] || { echo 'Run this script as root.'; exit 1; }
for command in docker nginx certbot python3 curl tar sha256sum; do
    command -v "$command" >/dev/null || { echo "Missing prerequisite: $command"; exit 1; }
done
docker compose version >/dev/null
install -d "$BASE"
exec 9>"$BASE/update.lock"
flock -w 180 9 || { echo "Another VFI deployment is running; try again after it finishes."; exit 1; }
if [ -e "$SITE" ] && ! grep -q '127.0.0.1:8796' "$SITE"; then
    echo "An unrelated site configuration exists at $SITE; nothing overwritten."
    exit 1
fi
if ss -ltnH 'sport = :8796' | grep -q .; then
    if ! docker ps --filter label=com.docker.compose.project=vfi-simulation --format '{{.Ports}}' | grep -q '8796'; then
        echo 'Port 8796 is occupied by another service; nothing stopped.'
        exit 1
    fi
fi
DIGEST=$(sha256sum /tmp/vfi-simulation-source.tar.gz | cut -c1-12)
RELEASE="$BASE/releases/bootstrap-$DIGEST"
install -d "$RELEASE" "$BASE/backups"
tar -xzf /tmp/vfi-simulation-source.tar.gz -C "$RELEASE"
if [ ! -f "$BASE/.env" ]; then
    python3 - "$BASE/.env" <<'PYENV'
from pathlib import Path
import secrets,sys
Path(sys.argv[1]).write_text('FAIRPASS_TEACHER_KEY='+secrets.token_urlsafe(48)+'\n')
PYENV
fi
chmod 600 "$BASE/.env"
if [ ! -d "$BASE/data" ]; then
    install -d -o 10001 -g 10001 -m 700 "$BASE/data"
fi
export VFI_ENV_FILE="$BASE/.env" VFI_DATA_DIR="$BASE/data"
export VFI_IMAGE="vfi-simulation:bootstrap-$DIGEST"
docker compose -p vfi-simulation -f "$RELEASE/compose.yaml" build
if docker ps --format '{{.Names}}' | grep -qx 'vfi-simulation-simulation-1'; then
    docker exec vfi-simulation-simulation-1 python -c "import sqlite3,datetime; p='/data/before-deploy-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'.sqlite3'; s=sqlite3.connect('/data/vfi.sqlite3'); d=sqlite3.connect(p); s.backup(d); result=d.execute('PRAGMA integrity_check').fetchone()[0]; d.close(); s.close(); print('Session backup:',p,'integrity:',result); assert result=='ok'"
fi
docker compose -p vfi-simulation -f "$RELEASE/compose.yaml" up -d --no-build
ID=$(docker compose -p vfi-simulation -f "$RELEASE/compose.yaml" ps -q simulation)
READY=0
for attempt in $(seq 1 60); do
    if [ "$(docker inspect --format '{{.State.Health.Status}}' "$ID")" = healthy ]; then READY=1; break; fi
    sleep 2
done
if [ "$READY" != 1 ]; then
    docker compose -p vfi-simulation -f "$RELEASE/compose.yaml" logs --tail=30
    echo 'Application health check failed. HTTPS setup stopped.'
    exit 1
fi
CERT_DIR="/etc/letsencrypt/live/$HOST"
SITE_BACKUP=""
if [ -e "$SITE" ]; then
    SITE_BACKUP="$BASE/backups/nginx-$(date +%Y%m%d%H%M%S).conf"
    cp -a "$SITE" "$SITE_BACKUP"
fi
if [ -f "$CERT_DIR/fullchain.pem" ] && [ -f "$CERT_DIR/privkey.pem" ]; then
    cat > "$SITE" <<'NGINX'
server {
    listen 80;
    listen [::]:80;
    server_name vfi.coursework.live;
    return 301 https://$host$request_uri;
}
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name vfi.coursework.live;
    ssl_certificate /etc/letsencrypt/live/vfi.coursework.live/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/vfi.coursework.live/privkey.pem;
NGINX
    REUSE_CERT=1
else
    cat > "$SITE" <<'NGINX'
server {
    listen 80;
    listen [::]:80;
    server_name vfi.coursework.live;
NGINX
    REUSE_CERT=0
fi
cat >> "$SITE" <<'NGINX'
    client_max_body_size 1m;
    add_header Cache-Control "no-store, no-cache, must-revalidate, max-age=0" always;
    add_header Pragma "no-cache" always;
    add_header Expires "0" always;
    location = /api/teacher-access { return 403; }
    location / {
        proxy_pass http://127.0.0.1:8796;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache off;
        proxy_buffering off;
        proxy_hide_header Cache-Control;
        proxy_read_timeout 120s;
    }
}
NGINX
if [ ! -e "/etc/nginx/sites-enabled/$HOST.conf" ]; then
    ln -s "$SITE" "/etc/nginx/sites-enabled/$HOST.conf"
fi
if ! nginx -t; then
    if [ -n "$SITE_BACKUP" ]; then
        cp -a "$SITE_BACKUP" "$SITE"
    else
        mv "$SITE" "$BASE/backups/rejected-nginx-$(date +%Y%m%d%H%M%S).conf"
        if [ -L "/etc/nginx/sites-enabled/$HOST.conf" ]; then unlink "/etc/nginx/sites-enabled/$HOST.conf"; fi
    fi
    echo 'Nginx validation failed; the previous site configuration was restored. Nothing reloaded.'
    exit 1
fi
systemctl reload nginx
if [ "$REUSE_CERT" = 0 ]; then
    certbot --nginx -d "$HOST" --redirect --keep-until-expiring
    nginx -t
else
    echo 'Reusing the existing HTTPS certificate; no Certbot renewal or selection prompt.'
fi
curl -fsS "https://$HOST/api/connection"
curl -fsS "https://$HOST/api/v4/content" -o /dev/null
printf '\n'
ln -sfn "$RELEASE" "$BASE/current"
printf '%s\n' "$VFI_IMAGE" > "$BASE/current-image"
printf 'bootstrap-%s\n' "$DIGEST" > "$BASE/published-commit"
install -m 700 "$RELEASE/deployment/update.sh" "$BASE/update.sh"
cat > /etc/cron.d/vfi-simulation-update <<'CRON'
* * * * * root /srv/keeper/services/vfi-simulation/update.sh >> /var/log/vfi-simulation-update.log 2>&1
CRON
chmod 644 /etc/cron.d/vfi-simulation-update
python3 - "$BASE" <<'PYLINK'
from pathlib import Path
import sys
base=Path(sys.argv[1])
key=next(x.split('=',1)[1].strip() for x in (base/'.env').read_text().splitlines() if x.startswith('FAIRPASS_TEACHER_KEY='))
link='https://vfi.coursework.live/?screen=teacher#'+key
(base/'teacher-link.txt').write_text(link+'\n')
(base/'teacher-link.txt').chmod(0o600)
print('\nPRIVATE TEACHER LINK â€” keep this to yourself:\n'+link)
print('\nStudent address: https://vfi.coursework.live')
PYLINK
if [ ! -f /root/.ssh/vfi_simulation_deploy ]; then
    echo 'The one-minute updater is installed, waiting for the GitHub deploy key and private repository.'
else
    echo 'The one-minute updater is installed; GitHub access will be checked on its next run.'
fi
