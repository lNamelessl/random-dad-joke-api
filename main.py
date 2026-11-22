"""Tiny random dad-joke API - single-file FastAPI app.

Endpoints:
    GET /joke    -> a random programming dad joke as JSON
    GET /health  -> {"ok": true}  (dotless healthcheck target)
    GET /jokes   -> the whole built-in joke list
    GET /        -> small HTML landing page with a fresh joke

Zero required environment variables. No dependencies beyond fastapi + uvicorn.
"""

import os
import random

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(
    title="Random Dad Joke API",
    description="A tiny API that returns a random programming dad joke.",
    version="1.0.0",
)

JOKES = [
    {"setup": "Why do programmers prefer dark mode?", "punchline": "Because light attracts bugs."},
    {"setup": "How many programmers does it take to change a light bulb?", "punchline": "None, that's a hardware problem."},
    {"setup": "Why did the developer go broke?", "punchline": "Because he used up all his cache."},
    {"setup": "What is a programmer's favorite hangout place?", "punchline": "Foo Bar."},
    {"setup": "Why do Java developers wear glasses?", "punchline": "Because they don't C#."},
    {"setup": "A SQL query walks into a bar, walks up to two tables and asks...", "punchline": "Can I join you?"},
    {"setup": "Why was the function sad after a hard day?", "punchline": "It didn't get any calls."},
    {"setup": "What do you call a programmer from Finland?", "punchline": "Nerdic."},
    {"setup": "Why did the programmer quit his job?", "punchline": "Because he didn't get arrays."},
    {"setup": "What's the object-oriented way to become wealthy?", "punchline": "Inheritance."},
    {"setup": "How does a computer get drunk?", "punchline": "It takes screenshots."},
    {"setup": "Why do Python programmers have low self-esteem?", "punchline": "They're constantly comparing their self to None."},
    {"setup": "What did the router say to the doctor?", "punchline": "It hurts when IP."},
    {"setup": "Why do programmers hate nature?", "punchline": "Too many bugs and no debugger."},
    {"setup": "Why was the JavaScript developer sad?", "punchline": "Because he didn't Node how to Express himself."},
    {"setup": "What do you call 8 hobbits?", "punchline": "A hobbyte."},
    {"setup": "Why did the developer go to therapy?", "punchline": "Too many unresolved issues."},
    {"setup": "What's the best thing about a Boolean?", "punchline": "Even if you're wrong, you're only off by a bit."},
    {"setup": "How do you comfort a JavaScript bug?", "punchline": "You console it."},
    {"setup": "Why did the API break up with the database?", "punchline": "Too many failed connections."},
]

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Random Dad Joke API</title>
<style>
  body { font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
         margin: 0; min-height: 100vh; display: grid; place-items: center;
         background: #0f172a; color: #e2e8f0; padding: 24px; }
  .card { max-width: 640px; width: 100%; background: #1e293b; border: 1px solid #334155;
          border-radius: 16px; padding: 32px; box-sizing: border-box; }
  h1 { margin: 0 0 8px; font-size: 1.5rem; }
  .sub { color: #94a3b8; font-size: 0.9rem; margin-bottom: 24px; }
  .joke { font-size: 1.15rem; line-height: 1.6; padding: 20px; background: #0f172a;
          border-left: 4px solid #38bdf8; border-radius: 8px; margin-bottom: 20px; }
  a.button { display: inline-block; background: #38bdf8; color: #0f172a; text-decoration: none;
             font-weight: 600; padding: 10px 18px; border-radius: 8px; }
  code { background: #0f172a; padding: 2px 6px; border-radius: 4px; color: #7dd3fc; }
  ul { color: #94a3b8; font-size: 0.9rem; line-height: 1.9; padding-left: 18px; }
</style>
</head>
<body>
  <div class="card">
    <h1>Random Dad Joke API</h1>
    <div class="sub">One tiny FastAPI service. No database, no secrets, no config.</div>
    <div class="joke">__JOKE__</div>
    <p><a class="button" href="/joke">Get another joke</a></p>
    <ul>
      <li><code>GET /joke</code> &mdash; one random programming dad joke</li>
      <li><code>GET /jokes</code> &mdash; the whole built-in list</li>
      <li><code>GET /health</code> &mdash; returns ok true</li>
      <li><code>GET /docs</code> &mdash; interactive OpenAPI docs</li>
    </ul>
  </div>
</body>
</html>
"""


def pick():
    """Return one random joke payload."""
    idx = random.randrange(len(JOKES))
    joke = JOKES[idx]
    text = joke["setup"] + " " + joke["punchline"]
    return {
        "id": idx,
        "joke": text,
        "setup": joke["setup"],
        "punchline": joke["punchline"],
        "total": len(JOKES),
    }


@app.get("/health")
def health():
    """Dotless healthcheck target - always 200 while the process is up."""
    return {"ok": True}


@app.get("/joke")
def get_joke():
    """Return one random programming dad joke."""
    return JSONResponse(content=pick())


@app.get("/jokes")
def list_jokes():
    """Return the full built-in joke list."""
    return {"count": len(JOKES), "jokes": JOKES}


@app.get("/")
def index():
    """Human-friendly landing page with a fresh joke."""
    html = PAGE.replace("__JOKE__", pick()["joke"])
    return HTMLResponse(content=html)


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
