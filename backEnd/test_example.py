"""
Example test cases for Football Analytics Backend.
Run with: pytest test_example.py
"""
import pytest
from httpx import AsyncClient
from datetime import date

# Base URL for tests
BASE_URL = "http://localhost:8000/api/v1"


class TestMatchesEndpoints:
    """Test matches/fixtures endpoints."""
    
    @pytest.mark.asyncio
    async def test_get_live_matches(self):
        """Test getting live matches."""
        async with AsyncClient(base_url=BASE_URL) as client:
            response = await client.get("/matches/live")
            assert response.status_code == 200
            data = response.json()
            assert "count" in data
            assert "fixtures" in data
    
    @pytest.mark.asyncio
    async def test_get_today_matches(self):
        """Test getting today's matches."""
        async with AsyncClient(base_url=BASE_URL) as client:
            response = await client.get("/matches/today")
            assert response.status_code == 200
            data = response.json()
            assert "date" in data
            assert "count" in data
            assert "fixtures" in data
    
    @pytest.mark.asyncio
    async def test_get_matches_by_date(self):
        """Test getting matches for a specific date."""
        test_date = "2024-10-24"
        async with AsyncClient(base_url=BASE_URL) as client:
            response = await client.get(f"/matches/date/{test_date}")
            assert response.status_code == 200
            data = response.json()
            assert data["date"] == test_date


class TestStandingsEndpoints:
    """Test standings endpoints."""
    
    @pytest.mark.asyncio
    async def test_get_premier_league_standings(self):
        """Test getting Premier League standings."""
        league_id = 39  # Premier League
        season = 2023
        
        async with AsyncClient(base_url=BASE_URL) as client:
            response = await client.get(
                f"/standings/{league_id}",
                params={"season": season}
            )
            
            if response.status_code == 200:
                data = response.json()
                assert data["league_id"] == league_id
                assert data["season"] == season
                assert "standings" in data
            else:
                # API might not have data or rate limit reached
                assert response.status_code in [404, 429, 500]


class TestStatisticsEndpoints:
    """Test statistics endpoints."""
    
    @pytest.mark.asyncio
    async def test_get_top_scorers(self):
        """Test getting top scorers."""
        league_id = 39  # Premier League
        season = 2023
        
        async with AsyncClient(base_url=BASE_URL) as client:
            response = await client.get(
                f"/statistics/top-scorers/{league_id}",
                params={"season": season}
            )
            
            if response.status_code == 200:
                data = response.json()
                assert data["league_id"] == league_id
                assert data["season"] == season
                assert "top_scorers" in data
    
    @pytest.mark.asyncio
    async def test_search_players(self):
        """Test player search."""
        query = "Messi"
        
        async with AsyncClient(base_url=BASE_URL) as client:
            response = await client.get(
                "/statistics/players/search",
                params={"query": query}
            )
            
            if response.status_code == 200:
                data = response.json()
                assert data["query"] == query
                assert "players" in data


class TestPredictionsEndpoints:
    """Test predictions endpoints."""
    
    @pytest.mark.asyncio
    async def test_get_predictions(self):
        """Test getting match predictions."""
        fixture_id = 12345  # Example fixture ID
        
        async with AsyncClient(base_url=BASE_URL) as client:
            response = await client.get(f"/predictions/{fixture_id}")
            
            # Predictions may not be available for all fixtures
            assert response.status_code in [200, 404, 500]
            
            if response.status_code == 200:
                data = response.json()
                assert data["fixture_id"] == fixture_id


class TestHealthCheck:
    """Test basic health and connectivity."""
    
    @pytest.mark.asyncio
    async def test_api_is_running(self):
        """Test that API is accessible."""
        async with AsyncClient(base_url="http://localhost:8000") as client:
            response = await client.get("/docs")
            assert response.status_code == 200


# Example: Manual test script (no pytest needed)
if __name__ == "__main__":
    import asyncio
    from httpx import AsyncClient
    
    async def quick_test():
        """Quick manual test."""
        print("Testing Football Analytics Backend...")
        print("=" * 50)
        
        async with AsyncClient(base_url=BASE_URL) as client:
            # Test 1: Get today's matches
            print("\n1. Getting today's matches...")
            response = await client.get("/matches/today")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Found {data['count']} matches today")
            else:
                print(f"   ❌ Error: {response.status_code}")
            
            # Test 2: Get live matches
            print("\n2. Getting live matches...")
            response = await client.get("/matches/live")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Found {data['count']} live matches")
            else:
                print(f"   ❌ Error: {response.status_code}")
            
            # Test 3: Get Premier League standings
            print("\n3. Getting Premier League standings...")
            response = await client.get(
                "/standings/39",
                params={"season": 2023}
            )
            if response.status_code == 200:
                data = response.json()
                if data["standings"]:
                    top_team = data["standings"][0][0]
                    print(f"   ✅ Top team: {top_team['team']['name']} "
                          f"({top_team['points']} pts)")
            else:
                print(f"   ❌ Error: {response.status_code}")
            
            # Test 4: Search for a player
            print("\n4. Searching for players...")
            response = await client.get(
                "/statistics/players/search",
                params={"query": "Haaland"}
            )
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Found {data['count']} players")
            else:
                print(f"   ❌ Error: {response.status_code}")
        
        print("\n" + "=" * 50)
        print("Tests completed!")
    
    # Run the quick test
    asyncio.run(quick_test())
