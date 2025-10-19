-- Football Analytics Database Schema for API-Football v3
-- File: db/db_schema.sql
-- Purpose: Create normalized PostgreSQL schema to ingest and analyze API-Football v3 data
-- Notes: UUIDs used for public-facing keys; serial integer surrogate keys for joins/compatibility.

-- Enable uuid-ossp if not already available (requires superuser)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- SCHEMA: public (default)

-- 1. Reference tables: competitions/leagues, seasons, rounds, groups
CREATE TABLE IF NOT EXISTS leagues (
	id            BIGINT PRIMARY KEY, -- API-Football league id
	name          TEXT NOT NULL,
	country       TEXT,
	country_code  VARCHAR(8),
	logo          TEXT,
	flag          TEXT,
	type          VARCHAR(64), -- league, cup, friendly, etc.
	created_at    TIMESTAMP WITH TIME ZONE DEFAULT now(),
	updated_at    TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS seasons (
	id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	league_id     BIGINT NOT NULL REFERENCES leagues(id) ON DELETE CASCADE,
	year          VARCHAR(20) NOT NULL, -- e.g. "2023/2024" or single-year '2024'
	start_date    DATE,
	end_date      DATE,
	coverage      JSONB, -- API coverage object
	created_at    TIMESTAMP WITH TIME ZONE DEFAULT now(),
	updated_at    TIMESTAMP WITH TIME ZONE DEFAULT now(),
	UNIQUE (league_id, year)
);

CREATE TABLE IF NOT EXISTS rounds (
	id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	season_id     UUID NOT NULL REFERENCES seasons(id) ON DELETE CASCADE,
	name          TEXT NOT NULL,
	round_order   INTEGER, -- ordering when applicable
	created_at    TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS groups (
	id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	season_id     UUID NOT NULL REFERENCES seasons(id) ON DELETE CASCADE,
	name          TEXT NOT NULL,
	created_at    TIMESTAMP WITH TIME ZONE DEFAULT now(),
	UNIQUE (season_id, name)
);

-- 2. Teams, coaches, venues
CREATE TABLE IF NOT EXISTS venues (
	id            BIGINT PRIMARY KEY, -- API stadium id if present
	name          TEXT,
	city          TEXT,
	capacity      INTEGER,
	surface       TEXT,
	address       TEXT,
	country       TEXT,
	latitude      NUMERIC(9,6),
	longitude     NUMERIC(9,6),
	country_code  VARCHAR(8),
	created_at    TIMESTAMP WITH TIME ZONE DEFAULT now(),
	updated_at    TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS teams (
	id            BIGINT PRIMARY KEY, -- API-Football team id
	name          TEXT NOT NULL,
	short_code    VARCHAR(16),
	country       TEXT,
	founded       INTEGER,
	national      BOOLEAN DEFAULT FALSE,
	logo          TEXT,
	venue_id      BIGINT REFERENCES venues(id) ON DELETE SET NULL,
	created_at    TIMESTAMP WITH TIME ZONE DEFAULT now(),
	updated_at    TIMESTAMP WITH TIME ZONE DEFAULT now(),
	UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS coaches (
	id            BIGINT PRIMARY KEY, -- API coach id if present
	team_id       BIGINT REFERENCES teams(id) ON DELETE CASCADE,
	firstname     TEXT,
	lastname      TEXT,
	name          TEXT,
	nationality   TEXT,
	birth_date    DATE,
	birth_place   TEXT,
	photo         TEXT,
	created_at    TIMESTAMP WITH TIME ZONE DEFAULT now(),
	updated_at    TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- 3. Players and profiles
CREATE TABLE IF NOT EXISTS players (
	id            BIGINT PRIMARY KEY, -- API player id
	firstname     TEXT,
	lastname      TEXT,
	name          TEXT,
	nationality   TEXT,
	birth_date    DATE,
	birth_place   TEXT,
	height        VARCHAR(16),
	weight        VARCHAR(16),
	photo         TEXT,
	created_at    TIMESTAMP WITH TIME ZONE DEFAULT now(),
	updated_at    TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- players can move teams across seasons; store contract periods in join table
CREATE TABLE IF NOT EXISTS player_team_seasons (
	id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	player_id     BIGINT NOT NULL REFERENCES players(id) ON DELETE CASCADE,
	team_id       BIGINT NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
	season_id     UUID NOT NULL REFERENCES seasons(id) ON DELETE CASCADE,
	number        INTEGER,
	position      VARCHAR(32), -- primary position during that season
	start_date    DATE,
	end_date      DATE,
	is_current    BOOLEAN DEFAULT FALSE,
	contract_info JSONB,
	UNIQUE (player_id, team_id, season_id)
);

-- 4. Fixtures (matches)
CREATE TABLE IF NOT EXISTS fixtures (
	id            BIGINT PRIMARY KEY, -- API fixture id
	league_id     BIGINT REFERENCES leagues(id) ON DELETE SET NULL,
	season_id     UUID REFERENCES seasons(id) ON DELETE SET NULL,
	round_id      UUID REFERENCES rounds(id) ON DELETE SET NULL,
	group_id      UUID REFERENCES groups(id) ON DELETE SET NULL,
	venue_id      BIGINT REFERENCES venues(id) ON DELETE SET NULL,
	referee       TEXT,
	event_date    TIMESTAMP WITH TIME ZONE, -- kickoff time
	status        VARCHAR(32), -- scheduled, live, finished, postponed, cancelled
	status_code   INTEGER,
	timestamp_utc TIMESTAMP WITH TIME ZONE,
	venue_info    JSONB,
	referee_info  JSONB,
	home_team_id  BIGINT NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
	away_team_id  BIGINT NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
	home_score    INTEGER,
	away_score    INTEGER,
	winner        INTEGER, -- 1 home, 2 away, 0 draw
	round_name    TEXT,
	attendance    INTEGER,
	weather       JSONB,
	created_at    TIMESTAMP WITH TIME ZONE DEFAULT now(),
	updated_at    TIMESTAMP WITH TIME ZONE DEFAULT now(),
	UNIQUE (league_id, season_id, id)
);

-- Link fixtures to teams in a join table to allow many-to-many meta (e.g., alternate team roles)
CREATE TABLE IF NOT EXISTS fixture_teams (
	fixture_id    BIGINT NOT NULL REFERENCES fixtures(id) ON DELETE CASCADE,
	team_id       BIGINT NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
	is_home       BOOLEAN NOT NULL,
	role          VARCHAR(32), -- e.g., 'home','away','neutral'
	PRIMARY KEY (fixture_id, team_id)
);

-- 5. Events (goals, cards, substitutions, shots, etc.)
CREATE TABLE IF NOT EXISTS events (
	id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	fixture_id    BIGINT NOT NULL REFERENCES fixtures(id) ON DELETE CASCADE,
	team_id       BIGINT REFERENCES teams(id) ON DELETE SET NULL,
	player_id     BIGINT REFERENCES players(id) ON DELETE SET NULL,
	assist_id     BIGINT REFERENCES players(id) ON DELETE SET NULL,
	event_type    VARCHAR(64) NOT NULL, -- goal, card, substitution, penalty, etc.
	detail        TEXT,
	minute        INTEGER,
	extra_minute  INTEGER,
	score         TEXT, -- e.g., '1-0'
	position      VARCHAR(32),
	outcome       VARCHAR(32),
	stats         JSONB, -- event-specific stats
	created_at    TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- 6. Lineups and substitutes
CREATE TABLE IF NOT EXISTS lineups (
	id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	fixture_id    BIGINT NOT NULL REFERENCES fixtures(id) ON DELETE CASCADE,
	team_id       BIGINT NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
	coach_id      BIGINT REFERENCES coaches(id) ON DELETE SET NULL,
	formation     VARCHAR(32),
	lineup        JSONB, -- store detailed lineup (positions, roles)
	bench         JSONB,
	created_at    TIMESTAMP WITH TIME ZONE DEFAULT now(),
	UNIQUE (fixture_id, team_id)
);

-- 7. Statistics
-- Player statistics per fixture
CREATE TABLE IF NOT EXISTS player_stats (
	id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	fixture_id    BIGINT NOT NULL REFERENCES fixtures(id) ON DELETE CASCADE,
	player_id     BIGINT NOT NULL REFERENCES players(id) ON DELETE CASCADE,
	team_id       BIGINT NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
	minutes_played INTEGER,
	rating        NUMERIC(4,2),
	shots         JSONB,
	passes        JSONB,
	tackles       JSONB,
	cards         JSONB,
	shots_total   INTEGER,
	shots_on_goal INTEGER,
	goals         INTEGER,
	assists       INTEGER,
	substitutions JSONB,
	stats_raw     JSONB,
	created_at    TIMESTAMP WITH TIME ZONE DEFAULT now(),
	UNIQUE (fixture_id, player_id)
);

-- Team statistics per fixture
CREATE TABLE IF NOT EXISTS team_stats (
	id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	fixture_id    BIGINT NOT NULL REFERENCES fixtures(id) ON DELETE CASCADE,
	team_id       BIGINT NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
	possession    NUMERIC(5,2),
	shots_total   INTEGER,
	shots_on_goal INTEGER,
	fouls         INTEGER,
	corners       INTEGER,
	offsides      INTEGER,
	lineup_snapshot JSONB,
	stats_raw     JSONB,
	created_at    TIMESTAMP WITH TIME ZONE DEFAULT now(),
	UNIQUE (fixture_id, team_id)
);

-- 8. Standings (tables) per season/league/group
CREATE TABLE IF NOT EXISTS standings (
	id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	league_id     BIGINT REFERENCES leagues(id) ON DELETE CASCADE,
	season_id     UUID REFERENCES seasons(id) ON DELETE CASCADE,
	group_id      UUID REFERENCES groups(id) ON DELETE CASCADE,
	team_id       BIGINT NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
	rank          INTEGER,
	played        INTEGER DEFAULT 0,
	wins          INTEGER DEFAULT 0,
	draws         INTEGER DEFAULT 0,
	losses        INTEGER DEFAULT 0,
	points        INTEGER DEFAULT 0,
	goals_for     INTEGER DEFAULT 0,
	goals_against INTEGER DEFAULT 0,
	goal_diff     INTEGER GENERATED ALWAYS AS (goals_for - goals_against) STORED,
	form          TEXT, -- e.g., "W W D L"
	details       JSONB,
	updated_at    TIMESTAMP WITH TIME ZONE DEFAULT now(),
	UNIQUE (league_id, season_id, group_id, team_id)
);

-- 9. Transfers
CREATE TABLE IF NOT EXISTS transfers (
	id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	player_id     BIGINT NOT NULL REFERENCES players(id) ON DELETE CASCADE,
	from_team_id  BIGINT REFERENCES teams(id) ON DELETE SET NULL,
	to_team_id    BIGINT REFERENCES teams(id) ON DELETE SET NULL,
	transfer_date DATE,
	type          VARCHAR(32), -- transfer, loan, end of loan
	fee           NUMERIC(12,2),
	details       JSONB,
	created_at    TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- 10. News items
CREATE TABLE IF NOT EXISTS news (
	id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	external_id   TEXT, -- id from source if available
	title         TEXT NOT NULL,
	summary       TEXT,
	content       TEXT,
	source        TEXT,
	url           TEXT,
	published_at  TIMESTAMP WITH TIME ZONE,
	tags          TEXT[],
	metadata      JSONB,
	created_at    TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- 11. Misc: mapping tables for many-to-many relations
CREATE TABLE IF NOT EXISTS team_group_memberships (
	id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	team_id       BIGINT NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
	group_id      UUID NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
	season_id     UUID NOT NULL REFERENCES seasons(id) ON DELETE CASCADE,
	UNIQUE (team_id, group_id, season_id)
);

-- 12. Audit / raw payloads to support re-ingestion and debugging
CREATE TABLE IF NOT EXISTS raw_payloads (
	id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	source        TEXT NOT NULL, -- endpoint name
	external_id   TEXT,
	received_at   TIMESTAMP WITH TIME ZONE DEFAULT now(),
	payload       JSONB
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_seasons_league_year ON seasons(league_id, year);
CREATE INDEX IF NOT EXISTS idx_fixtures_event_date ON fixtures(event_date);
CREATE INDEX IF NOT EXISTS idx_fixtures_league_season ON fixtures(league_id, season_id);
CREATE INDEX IF NOT EXISTS idx_events_fixture_minute ON events(fixture_id, minute);
CREATE INDEX IF NOT EXISTS idx_player_stats_fixture_player ON player_stats(fixture_id, player_id);
CREATE INDEX IF NOT EXISTS idx_team_stats_fixture_team ON team_stats(fixture_id, team_id);
CREATE INDEX IF NOT EXISTS idx_standings_league_season_rank ON standings(league_id, season_id, rank);

-- Composite index: find fixtures for a team quickly
CREATE INDEX IF NOT EXISTS idx_fixtures_team_event_date ON fixtures(home_team_id, away_team_id, event_date);

-- Example trigger: Update standings when a fixture result is inserted/updated (simple approach)
-- We'll store a lightweight function that recalculates standings for the affected league/season/group and teams.

CREATE OR REPLACE FUNCTION recalc_standings_for_fixture() RETURNS TRIGGER AS $$
DECLARE
	f_record RECORD;
BEGIN
	-- Only process when status is 'finished' and scores are present
	IF (TG_OP = 'INSERT' OR TG_OP = 'UPDATE') THEN
		SELECT * INTO f_record FROM fixtures WHERE id = NEW.id;
		IF (f_record.status IS NOT NULL AND lower(f_record.status) = 'finished') THEN
			-- For simplicity, mark standings as needing refresh by updating updated_at on standings rows for the teams
			UPDATE standings SET updated_at = now() WHERE team_id IN (f_record.home_team_id, f_record.away_team_id)
			  AND season_id = f_record.season_id;
		END IF;
	ELSIF TG_OP = 'DELETE' THEN
		NULL; -- ignore
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach trigger to fixtures table
DROP TRIGGER IF EXISTS trg_recalc_standings_on_fixture ON fixtures;
CREATE TRIGGER trg_recalc_standings_on_fixture
AFTER INSERT OR UPDATE ON fixtures
FOR EACH ROW EXECUTE FUNCTION recalc_standings_for_fixture();

-- Example: function to fully recompute standings for a league/season/group (can be called offline)
CREATE OR REPLACE FUNCTION compute_standings(p_league_id BIGINT, p_season_id UUID, p_group_id UUID) RETURNS VOID AS $$
DECLARE
	r RECORD;
BEGIN
	-- Reset computed fields for the relevant teams
	DELETE FROM standings WHERE league_id = p_league_id AND season_id = p_season_id AND (p_group_id IS NULL OR group_id = p_group_id);

	-- Aggregate results from fixtures marked 'finished'
	FOR r IN
		SELECT t.id AS team_id
		FROM teams t
		JOIN fixture_teams ft ON ft.team_id = t.id
		JOIN fixtures f ON f.id = ft.fixture_id
		WHERE f.league_id = p_league_id AND f.season_id = p_season_id
		AND (p_group_id IS NULL OR ft.team_id IN (SELECT team_id FROM team_group_memberships WHERE group_id = p_group_id AND season_id = p_season_id))
		GROUP BY t.id
	LOOP
		-- compute aggregates for team r.team_id
		INSERT INTO standings (id, league_id, season_id, group_id, team_id, played, wins, draws, losses, points, goals_for, goals_against, form, details, updated_at)
		SELECT uuid_generate_v4(), p_league_id, p_season_id, p_group_id, r.team_id,
			COALESCE(SUM(CASE WHEN f.status = 'finished' AND (f.home_team_id = r.team_id OR f.away_team_id = r.team_id) THEN 1 ELSE 0 END),0) as played,
			COALESCE(SUM(CASE WHEN f.status = 'finished' AND ((f.home_team_id = r.team_id AND f.winner = 1) OR (f.away_team_id = r.team_id AND f.winner = 2)) THEN 1 ELSE 0 END),0) as wins,
			COALESCE(SUM(CASE WHEN f.status = 'finished' AND f.winner = 0 AND (f.home_team_id = r.team_id OR f.away_team_id = r.team_id) THEN 1 ELSE 0 END),0) as draws,
			COALESCE(SUM(CASE WHEN f.status = 'finished' AND ((f.home_team_id = r.team_id AND f.winner = 2) OR (f.away_team_id = r.team_id AND f.winner = 1)) THEN 1 ELSE 0 END),0) as losses,
			COALESCE(SUM(CASE WHEN f.status = 'finished' AND ((f.home_team_id = r.team_id AND f.winner = 1) OR (f.away_team_id = r.team_id AND f.winner = 2)) THEN 3 WHEN f.status = 'finished' AND f.winner = 0 AND (f.home_team_id = r.team_id OR f.away_team_id = r.team_id) THEN 1 ELSE 0 END),0) as points,
			COALESCE(SUM(CASE WHEN f.status = 'finished' AND f.home_team_id = r.team_id THEN f.home_score WHEN f.status = 'finished' AND f.away_team_id = r.team_id THEN f.away_score ELSE 0 END),0) as goals_for,
			COALESCE(SUM(CASE WHEN f.status = 'finished' AND f.home_team_id = r.team_id THEN f.away_score WHEN f.status = 'finished' AND f.away_team_id = r.team_id THEN f.home_score ELSE 0 END),0) as goals_against,
			NULL::text as form,
			jsonb_build_object('computed_at', now()) as details,
			now()
		FROM fixtures f
		WHERE (f.home_team_id = r.team_id OR f.away_team_id = r.team_id)
		  AND f.league_id = p_league_id
		  AND f.season_id = p_season_id;
	END LOOP;

	-- Rank teams
	UPDATE standings s SET rank = sub.rnk
	FROM (
		SELECT id, ROW_NUMBER() OVER (ORDER BY points DESC, goal_diff DESC, goals_for DESC) as rnk
		FROM standings
		WHERE league_id = p_league_id AND season_id = p_season_id AND (p_group_id IS NULL OR group_id = p_group_id)
	) as sub
	WHERE s.id = sub.id;
END;
$$ LANGUAGE plpgsql;

-- End of schema

