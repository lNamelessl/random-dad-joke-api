# Random Dad Joke API

**A tiny FastAPI service that returns a random programming dad joke as JSON — zero config, zero secrets, zero prompts.**

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/random-dad-joke-api)

## After deploying (5 steps)

1. Click **Deploy**. Railway prompts for nothing — there are no variables to fill in.
2. Wait for the build to finish; the release is gated on `GET /health` returning `200`.
3. Open your service's public domain (Railway → your service → **Settings → Networking → Generate Domain** if one is not already shown).
4. Call `https://YOUR-DOMAIN/health` → you get `{"ok": true}`.
5. Call `https://YOUR-DOMAIN/joke` → you get a random joke as JSON. Refresh for a new one.

Useful extras on the same domain: `/jokes` (full built-in list), `/docs` (OpenAPI UI), `/` (small HTML page).

```bash
curl -s https://YOUR-DOMAIN/joke
# {"id":11,"joke":"How does a computer get drunk? It takes screenshots.","setup":"How does a computer get drunk?","punchline":"It takes screenshots.","total":20}
```

## Sourcing and configuration

| Value | Where the user gets it | Where it lands |
| --- | --- | --- |
| PORT | Injected by Railway automatically | Read by the container start command (`PORT` defaults to 8000); do not set it |
| Everything else | Not applicable | There are **no required or optional environment variables** |

No API keys, no database URL, no domains to type in. The deploy form is empty by design.

## Honest limits (measured)

| Limit | Measured value | Notes |
| --- | --- | --- |
| Joke count | 20 built-in | A Python list in `main.py`; edit the file to add more |
| Response size | about 250 bytes | Single JSON object per `/joke` call |
| Cold start | about 1.5 s container boot to first 200 | `python:3.12-slim` plus uvicorn, measured on a fresh deploy |
| State | None | Stateless; restarts lose nothing, no volume mounted |
| Persistence | None | Same random distribution after every restart |
| Concurrency | Single uvicorn worker | Enough for demos; add `--workers` if you need more |

# Deploy and Host

Deploy the repo on Railway and it builds the Dockerfile, runs uvicorn on the injected
`PORT`, and serves `/joke`, `/jokes`, `/health`, and `/` on a generated HTTPS domain.
The release is healthcheck-gated: Railway polls the dotless `health` path and only marks
the deploy successful once it answers `200`.

## About Hosting

The whole service is one file, `main.py`, with `fastapi` and `uvicorn[standard]` as the only
dependencies (pinned in `requirements.txt`, installed in the `python:3.12-slim` image).
Jokes are an in-memory list, so there is no database, no volume, and no migration step.
`railway.json` pins `healthcheckPath: "health"`, a 300 s healthcheck timeout, and an
`ON_FAILURE` restart policy. Because no environment variables are required, there is no
"missing config" state and nothing to configure: the app answers correctly the moment the
container starts.

## Why Deploy

You get a permanently available, HTTPS JSON endpoint you can point a bot, tutorial, or
monitor at in under two minutes — no local server to keep running, no accounts to create,
no keys to rotate.

## Common Use Cases

- A random-joke source for Slack/Discord bots, browser extensions, or CLI toys.
- A minimal FastAPI skeleton to fork as the base of a real API.
- An always-on synthetic-monitoring or uptime target with a trivial `/health` contract.
- A first Railway deployment to learn builds, domains, and healthcheck gating.

## Dependencies for

### Deployment Dependencies

- Docker build from the repo-root `Dockerfile` (`python:3.12-slim`).
- `fastapi` and `uvicorn[standard]`, pinned in `requirements.txt`.
- No database, no volume, no secrets, and no environment variables — `PORT` is supplied by
  Railway at runtime and defaults to `8000` when absent.
