# Random Dad Joke API

A tiny, single-file FastAPI service that returns a random programming dad joke as JSON.
No database, no config, no required environment variables — clone/deploy and call it.

## Endpoints

| Method | Path | Response |
| --- | --- | --- |
| GET | `/joke` | `{"id": 7, "joke": "...", "setup": "...", "punchline": "...", "total": 20}` |
| GET | `/jokes` | `{"count": 20, "jokes": [...]}` — the whole built-in list |
| GET | `/health` | `{"ok": true}` — dotless healthcheck target |
| GET | `/` | Small HTML page with a joke and links |
| GET | `/docs` | Interactive OpenAPI docs (FastAPI default) |

Example:

```bash
curl -s https://YOUR-DOMAIN/joke
# {"id":3,"joke":"Why did the developer go broke? Because he used up all his cache.","setup":"...","punchline":"...","total":20}
```

## Run locally

```bash
pip install fastapi uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
curl -s localhost:8000/health   # {"ok":true}
curl -s localhost:8000/joke
```

Or with Docker:

```bash
docker build -t dad-joke-api .
docker run -p 8000:8000 dad-joke-api
```

The container reads `PORT` when Railway injects it and falls back to `8000` otherwise.
`railway.json` pins the healthcheck to the relative, dotless path `health`.

# Deploy and Host

Click Deploy: Railway builds the Dockerfile, starts uvicorn, and gates the release on
`GET /health` returning `{"ok": true}`. There are no prompts and nothing to fill in.

## About Hosting

The app is one `main.py` file served by uvicorn on the port Railway provides. Jokes live in
a Python list in memory, so the service is stateless and needs no volume, database, or
secrets. A public HTTPS domain is generated automatically.

## Why Deploy

You want a working JSON API to point at from a tutorial, a Slack bot, a demo, or a
health-check experiment — without provisioning anything.

## Common Use Cases

- A random-joke source for chat bots and browser extensions.
- A minimal FastAPI reference skeleton for talks and tutorials.
- An uptime/synthetic-monitoring target with a trivially verifiable `/health`.
- A first Railway deploy to learn the platform on something tiny.

## Dependencies for

### Deployment Dependencies

- Python 3.12 (provided by the image `python:3.12-slim` in the Dockerfile).
- `fastapi` and `uvicorn[standard]` from `requirements.txt` — nothing else.
- Zero environment variables required. `PORT` is injected by Railway at runtime.
