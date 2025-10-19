-- Example queries for Football Analytics schema
-- File: db/example_queries.sql

-- 1) Last 5 matches for a team (by team id)
-- Uses idx_fixtures_team_event_date index
PREPARE last5matches (BIGINT) AS
SELECT id, event_date, home_team_id, away_team_id, home_score, away_score, status
FROM fixtures
WHERE (home_team_id = $1 OR away_team_id = $1)
ORDER BY event_date DESC
LIMIT 5;

-- Usage: EXECUTE last5matches(12345);

-- 2) Top scoring players in a season (league + season)
-- Uses player_stats and fixtures join; ensure fixtures have season_id populated
PREPARE top_scorers_in_season (BIGINT, UUID, INT) AS
SELECT p.id AS player_id, p.name AS player_name, SUM(ps.goals) AS goals
FROM player_stats ps
JOIN players p ON p.id = ps.player_id
JOIN fixtures f ON f.id = ps.fixture_id
WHERE f.league_id = $1 AND f.season_id = $2
GROUP BY p.id, p.name
ORDER BY goals DESC
LIMIT $3;

-- Usage: EXECUTE top_scorers_in_season(39, 'uuid-...', 10);

-- 3) League table snapshot (top 10)
-- Uses standings index idx_standings_league_season_rank
PREPARE league_table_snapshot (BIGINT, UUID, INT) AS
SELECT s.rank, t.name AS team_name, s.played, s.wins, s.draws, s.losses, s.points, s.goals_for, s.goals_against, s.goal_diff
FROM standings s
JOIN teams t ON t.id = s.team_id
WHERE s.league_id = $1 AND s.season_id = $2
ORDER BY s.rank ASC
LIMIT $3;

-- 4) Head-to-head last meetings between two teams
PREPARE head_to_head (BIGINT, BIGINT, INT) AS
SELECT f.id, f.event_date, f.home_team_id, f.away_team_id, f.home_score, f.away_score
FROM fixtures f
WHERE (f.home_team_id = $1 AND f.away_team_id = $2) OR (f.home_team_id = $2 AND f.away_team_id = $1)
ORDER BY f.event_date DESC
LIMIT $3;

-- 5) Player season totals (minutes, goals, assists, average rating)
PREPARE player_season_totals (BIGINT, UUID) AS
SELECT p.id AS player_id, p.name,
       SUM(COALESCE(ps.minutes_played,0)) AS minutes_played,
       SUM(COALESCE(ps.goals,0)) AS goals,
       SUM(COALESCE(ps.assists,0)) AS assists,
       ROUND(AVG(ps.rating)::numeric,2) AS avg_rating
FROM player_stats ps
JOIN players p ON p.id = ps.player_id
JOIN fixtures f ON f.id = ps.fixture_id
WHERE p.id = $1 AND f.season_id = $2
GROUP BY p.id, p.name;

-- 6) Recent events (goals) in last 24 hours across competitions
PREPARE recent_goals AS
SELECT e.id, e.fixture_id, e.team_id, e.player_id, e.minute, e.extra_minute, e.score
FROM events e
JOIN fixtures f ON f.id = e.fixture_id
WHERE e.event_type ILIKE 'goal%'
  AND f.event_date >= now() - interval '24 hours'
ORDER BY f.event_date DESC, e.minute DESC;

-- 7) Suggested materialized view for current standings
-- CREATE MATERIALIZED VIEW current_standings AS
-- SELECT * FROM standings WHERE updated_at >= (now() - interval '1 day');

-- Explain index usage notes:
-- - idx_fixtures_team_event_date accelerates queries that filter on a team's fixtures and order by date.
-- - idx_fixtures_league_season helps queries that restrict by league and season (e.g., top scorers per season).
-- - idx_player_stats_fixture_player helps point lookups for player + fixture combinations.

-- End of example queries
