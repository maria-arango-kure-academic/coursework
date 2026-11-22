# brewery-blob — anonymous JSON blob store for Keeper

Single-file Python service. Stdlib only. ~150 lines. CORS-enabled. Stores each blob as one JSON file on disk.

Mirrors the jsonblob.com API shape so `storage.js` in the brewery simulation can point at this service with a one-line change.

## Endpoints

```
POST   /api/blob          create a blob, body is JSON, returns {id, location}
GET    /api/blob/<id>     read a blob
PUT    /api/blob/<id>     replace a blob, body is JSON
DELETE /api/blob/<id>     delete a blob
GET    /healthz           liveness check
```

## Deploy on Keeper (3-step path)

Replace `brew.wellandgood.tech` with whatever subdomain you wire up.

### 1. Copy the folder onto Keeper

```bash
# from your laptop, in this repo
rsync -a teaching/courses/change-management/brewery-simulation/keeper-blob-server/ \
      keeper:/srv/keeper/services/brewery-blob/
```

### 2. Bring the container up

```bash
ssh keeper
cd /srv/keeper/services/brewery-blob
docker compose up -d --build
docker compose logs --tail=20
curl -s http://127.0.0.1:8088/healthz
# {"ok": true}
```

### 3. Wire up the reverse proxy

If Keeper uses Caddy (most likely, given Penpot's setup), add a block like this to your Caddyfile:

```
brew.wellandgood.tech {
    reverse_proxy 127.0.0.1:8088
}
```

Then `caddy reload` (or whatever your Caddy unit does on config change).

If Keeper uses nginx instead:

```nginx
server {
    listen 443 ssl;
    server_name brew.wellandgood.tech;

    # ssl certs (managed by certbot or similar)

    location / {
        proxy_pass http://127.0.0.1:8088;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Test from your laptop:

```bash
curl -s https://brew.wellandgood.tech/healthz
# {"ok": true}

curl -s -X POST https://brew.wellandgood.tech/api/blob \
  -H 'Content-Type: application/json' \
  -d '{"hello": "world"}'
# {"id": "AbC123_xy", "location": "/api/blob/AbC123_xy"}
```

### 4. Point the simulation at the new URL

In `teaching/courses/change-management/brewery-simulation/content.js`, find:

```js
storage: {
  base: "https://jsonblob.com/api/jsonBlob",
  pollSeconds: 6
}
```

Change to:

```js
storage: {
  base: "https://brew.wellandgood.tech/api/blob",
  pollSeconds: 6
}
```

Commit and push. GitHub Pages will serve the new version within a minute or two.

## Operations

- Data lives in `/srv/keeper/services/brewery-blob/data/` on the host. Each session and team is one JSON file.
- Snapshot the data: `cp -a /srv/keeper/services/brewery-blob/data /backup/...`
- Reset everything: `docker compose down && rm -rf data/*.json && docker compose up -d`
- Tighten CORS: set `BLOB_ALLOW_ORIGIN=https://<your-pages-url>` in `docker-compose.yml` and `docker compose up -d`.

## Security note

This is anonymous, public read+write. Anyone with a blob ID can read or overwrite it. That is fine for a 30 to 40 minute classroom exercise with anonymized data (brewery names, decisions, no personal info). For longer-lived storage, add a write key or move to a real auth-backed service.
