from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path


app = FastAPI(title="Football Analytics API")


# Allow local dev
app.add_middleware( CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Serve the frontend (frontEnd/) as static files so you can open http://localhost:8000
frontend_dir = Path(__file__).resolve().parent.parent / "frontEnd"
app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="static")


# ---------- Demo data (replace with your real data / API-Football bridge) ----------
LEAGUES = [
    {"id": 39, "name": "Premier League", "country": "England", "season": 2024, "logo": ""},
    {"id": 140, "name": "La Liga", "country": "Spain", "season": 2024, "logo": ""},
]


MATCHES = [
    {
    "id": 1001,
    "league": {"id": 39, "name": "Premier League", "country": "England", "logo": ""},
    "home": {"name": "Arsenal", "logo": ""},
    "away": {"name": "Chelsea", "logo": ""},
    "score": {"home": 2, "away": 1},
    "status": {"short": "LIVE"},
    "minute": 63,
    "kickoff_local": "13:00",
    "country": "England",
    "venue": "Emirates Stadium",
    "events": [
    {"minute": 17, "type": "Goal", "text": "Saka scores (1–0)"},
    {"minute": 38, "type": "Goal", "text": "Palmer equalizes (1–1)"},
    {"minute": 56, "type": "Goal", "text": "Ødegaard (2–1)"},
],
},
{
"id": 1002,
"league": {"id": 140, "name": "La Liga", "country": "Spain", "logo": ""},
"home": {"name": "Real Madrid", "logo": ""},
"away": {"name": "Sevilla", "logo": ""},
"score": {"home": None, "away": None},
"status": {"short": "NS"},
"kickoff_local": "15:30",
"country": "Spain",
"venue": "Bernabéu",
"events": [],
},
]


STANDINGS = {
39: [
    {"team": "Arsenal", "played": 8, "win": 6, "draw": 1, "loss": 1, "goals_for": 15, "goals_against": 6, "points": 19}]
}

@app.get("/leagues")
def get_leagues():
    return LEAGUES


@app.get("/matches")
def get_matches(date: str | None = None, live: bool | None = None, country: str | None = None, league_id: int | None = None):
    data = MATCHES
    if live:
        data = [m for m in data if m.get("status", {}).get("short") == "LIVE"]
    if country:
        data = [m for m in data if m.get("country") == country]
    if league_id:
        data = [m for m in data if (m.get("league") or {}).get("id") == league_id]
    return data


@app.get("/standings")
def get_standings(league_id: int):
    return STANDINGS.get(league_id, [])


@app.get("/match/{match_id}")
def get_match(match_id: int):
    for m in MATCHES:
        if m["id"] == match_id:
            return m
    return {"detail": "Not found"}


@app.get("/search")
def search(q: str):
    ql = q.lower()
    teams = []
    for m in MATCHES:
        for side in (m["home"], m["away"]):
            if ql in side["name"].lower():
                teams.append({"id": f"team:{side['name']}", "name": side["name"]})
    # dedupe
    seen = set(); unique = []
    for t in teams:
        if t["name"] not in seen:
            seen.add(t["name"]); unique.append(t)
            return {"teams": unique}
