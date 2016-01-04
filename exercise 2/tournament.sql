-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (
	id	SERIAL PRIMARY KEY,
	name 	VARCHAR NOT NULL
);

CREATE TABLE matches (
	id	SERIAL PRIMARY KEY,
	winner	INT REFERENCES players(id),
	loser	INT REFERENCES players(id)
);

CREATE VIEW base_standings AS
	SELECT
		p.id AS id,
		p.name AS name,
		CASE WHEN w.wins IS NULL THEN 0 ELSE w.wins END AS wins,
		-- Combines wins and losses to find mathes played
		CASE WHEN l.losses IS NULL THEN 0 ELSE l.losses END +
			CASE WHEN w.wins IS NULL THEN 0 ELSE w.wins END AS matches
	FROM
		(SELECT id, name
		FROM players) AS p
	-- Find player's wins and join on id
	LEFT JOIN
		(SELECT winner, COUNT(winner) AS wins
		FROM matches
		GROUP BY winner ) AS w
	ON w.winner = p.id
	-- Find player's losses and join on id
	LEFT JOIN
		(SELECT loser, COUNT(loser) AS losses
		FROM matches
		GROUP BY loser ) AS l
	ON l.loser = p.id
	ORDER BY wins;

CREATE VIEW standings AS
	SELECT
		s.id AS id,
		s.name AS name,
		s.wins AS wins,
		s.matches AS matches
	FROM base_standings AS s
	-- Join back on base_stands to rank by opponent's wins
	LEFT JOIN
		(SELECT
			m.winner AS winner,
			-- Sum wins made by opponents
			SUM(s.wins) AS owins
		FROM matches AS m
		LEFT JOIN base_standings AS s
		ON m.loser = s.id
		GROUP BY m.winner) AS omw
	ON s.id = omw.winner
	ORDER BY s.wins, omw.owins;

CREATE VIEW pairings AS
	SELECT 
		a.id AS a_id, 
		a.name AS a_name, 
		b.id AS b_id, 
		b.name AS b_name
	FROM
		-- Find position based on wins
		(SELECT 
			id AS id, 
			name AS name, 
			row_number() OVER (ORDER BY wins DESC) AS position
		FROM standings) AS a
	-- Join on self, but with position - 1
	INNER JOIN
		(SELECT 
			id, 
			name, 
			row_number() OVER (ORDER BY wins DESC) - 1 AS position
		FROM standings) AS b
	ON a.position = b.position
	-- Eliminate even numbered positions to remove double bookings
	WHERE a.position % 2 != 0;