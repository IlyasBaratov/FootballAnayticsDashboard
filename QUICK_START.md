# 🚀 Quick Start Guide - Football Analytics Backend

## Getting Started in 5 Minutes

### 1. Get Your API Key

1. Visit [API-Football](https://www.api-football.com/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Free tier includes: **100 requests/day**, **10 requests/minute**

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API key
# Replace 'your_api_key_here' with your actual API key
API_FOOTBALL_KEY=your_actual_api_key_here
```

### 3. Install Dependencies

```bash
cd backEnd
pip install -r requirements.txt
```

### 4. Setup Database

```bash
# Create PostgreSQL database
createdb football_analytics

# Run schema
psql -d football_analytics -f ../db/db_schema.sql
```

### 5. Start the Server

```bash
# From backEnd directory
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server will start at: `http://localhost:8000`

### 6. Test the API

**Open in browser:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

**Try these endpoints:**

```bash
# Get today's matches
curl http://localhost:8000/api/v1/matches/today

# Get live matches
curl http://localhost:8000/api/v1/matches/live

# Get Premier League standings 2023
curl http://localhost:8000/api/v1/standings/39?season=2023

# Get top scorers
curl http://localhost:8000/api/v1/statistics/top-scorers/39?season=2023
```

---

## 📝 Example Requests

### 1. Live Matches

**Request:**
```bash
curl http://localhost:8000/api/v1/matches/live
```

**Response:**
```json
{
  "count": 3,
  "fixtures": [
    {
      "fixture": {
        "id": 12345,
        "date": "2024-10-24T19:00:00+00:00",
        "status": {
          "long": "First Half",
          "short": "1H",
          "elapsed": 23
        }
      },
      "league": {
        "id": 39,
        "name": "Premier League",
        "country": "England"
      },
      "teams": {
        "home": {
          "id": 33,
          "name": "Manchester United",
          "logo": "..."
        },
        "away": {
          "id": 50,
          "name": "Manchester City",
          "logo": "..."
        }
      },
      "goals": {
        "home": 1,
        "away": 1
      }
    }
  ]
}
```

### 2. League Standings

**Request:**
```bash
curl http://localhost:8000/api/v1/standings/39?season=2023
```

**Response:**
```json
{
  "league_id": 39,
  "season": 2023,
  "standings": [[
    {
      "rank": 1,
      "team": {
        "id": 50,
        "name": "Manchester City"
      },
      "points": 89,
      "goalsDiff": 61,
      "all": {
        "played": 38,
        "win": 28,
        "draw": 5,
        "lose": 5,
        "goalsFor": 96,
        "goalsAgainst": 35
      }
    }
  ]]
}
```

### 3. Team Fixtures

**Request:**
```bash
curl "http://localhost:8000/api/v1/matches/team/33?next=5"
```

Gets next 5 fixtures for Manchester United (ID: 33)

### 4. Match Predictions

**Request:**
```bash
curl http://localhost:8000/api/v1/predictions/12345
```

**Response includes:**
- Win probability for each team
- Goals predictions
- Form comparison
- Head-to-head history

---

## 🎯 Common Use Cases

### Use Case 1: Display Today's Matches on Homepage

```python
import httpx
import asyncio

async def get_todays_matches():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/api/v1/matches/today"
        )
        return response.json()

# Use in your app
matches = asyncio.run(get_todays_matches())
print(f"Today's matches: {matches['count']}")
```

### Use Case 2: Build a League Standings Widget

```python
async def get_standings(league_id: int, season: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://localhost:8000/api/v1/standings/{league_id}",
            params={"season": season}
        )
        return response.json()

# Premier League 2023
standings = asyncio.run(get_standings(39, 2023))
for team in standings["standings"][0][:5]:  # Top 5
    print(f"{team['rank']}. {team['team']['name']} - {team['points']} pts")
```

### Use Case 3: Player Search

```python
async def search_player(name: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/api/v1/statistics/players/search",
            params={"query": name}
        )
        return response.json()

# Search for Messi
players = asyncio.run(search_player("Messi"))
```

### Use Case 4: Match Details with Stats

```python
async def get_match_details(fixture_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://localhost:8000/api/v1/matches/{fixture_id}",
            params={
                "include_statistics": True,
                "include_events": True,
                "include_lineups": True
            }
        )
        return response.json()

# Get full match details
match = asyncio.run(get_match_details(12345))
```

---

## 🌐 Frontend Integration

### React Example

```javascript
// Get live matches
const getLiveMatches = async () => {
  const response = await fetch(
    'http://localhost:8000/api/v1/matches/live'
  );
  const data = await response.json();
  return data.fixtures;
};

// Component
function LiveMatches() {
  const [matches, setMatches] = useState([]);

  useEffect(() => {
    getLiveMatches().then(setMatches);
    // Refresh every 30 seconds
    const interval = setInterval(() => {
      getLiveMatches().then(setMatches);
    }, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      {matches.map(match => (
        <MatchCard key={match.fixture.id} match={match} />
      ))}
    </div>
  );
}
```

### Vue.js Example

```javascript
// composables/useMatches.js
export const useMatches = () => {
  const matches = ref([]);
  const loading = ref(false);

  const fetchLiveMatches = async () => {
    loading.value = true;
    try {
      const response = await fetch(
        'http://localhost:8000/api/v1/matches/live'
      );
      const data = await response.json();
      matches.value = data.fixtures;
    } finally {
      loading.value = false;
    }
  };

  return { matches, loading, fetchLiveMatches };
};
```

---

## 🐳 Docker Quick Start

```bash
# Build and run everything
docker-compose up --build

# API will be available at http://localhost:8000
# Database will be on localhost:5432
```

---

## 📊 Popular League IDs Reference

| League | ID |
|--------|-----|
| **England** | |
| Premier League | 39 |
| Championship | 40 |
| **Spain** | |
| La Liga | 140 |
| Segunda División | 141 |
| **Germany** | |
| Bundesliga | 78 |
| 2. Bundesliga | 79 |
| **Italy** | |
| Serie A | 135 |
| Serie B | 136 |
| **France** | |
| Ligue 1 | 61 |
| Ligue 2 | 62 |
| **Europe** | |
| Champions League | 2 |
| Europa League | 3 |
| Conference League | 848 |
| **International** | |
| World Cup | 1 |
| Euro Championship | 4 |

[Full list](https://www.api-football.com/documentation-v3#tag/Leagues)

---

## 💡 Pro Tips

### 1. Minimize API Calls
- Cache responses (default: 5 minutes)
- Use database for historical data
- Batch requests when possible

### 2. Rate Limit Management
```python
# The client automatically handles rate limiting
# But you can adjust in .env:
API_FOOTBALL_RATE_LIMIT=10  # requests per minute
```

### 3. Monitor API Usage
Check your API usage at: https://www.api-football.com/

### 4. Upgrade When Needed
Free tier limits:
- ✅ 100 requests/day
- ✅ 10 requests/minute

Paid plans offer:
- 🚀 Up to 1,000,000 requests/day
- 🚀 No rate limits

---

## 🆘 Troubleshooting

### Issue: "API_FOOTBALL_KEY must be set"
**Solution:** Add your API key to `.env` file

### Issue: Rate limit exceeded
**Solution:** 
- Wait 1 minute for free tier
- Implement caching
- Upgrade plan

### Issue: Database connection error
**Solution:**
```bash
# Check PostgreSQL is running
pg_isready

# Check connection string in .env
DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/football_analytics
```

### Issue: Import errors
**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 📚 Next Steps

1. **Explore API docs:** Visit `http://localhost:8000/docs`
2. **Read full documentation:** See `API_DOCUMENTATION.md`
3. **Check database schema:** See `db/db_schema.sql`
4. **Build frontend:** Connect your React/Vue/Angular app

---

## 🤝 Need Help?

- 📖 [Full API Documentation](./API_DOCUMENTATION.md)
- 🌐 [API-Football Docs](https://www.api-football.com/documentation-v3)
- 🚀 [FastAPI Docs](https://fastapi.tiangolo.com/)

---

Happy Coding! ⚽🎯
