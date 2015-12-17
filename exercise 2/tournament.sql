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
	name 	varchar(30) NOT NULL
);
CREATE TABLE matches (
	id	SERIAL PRIMARY KEY,
	winner	int,
	loser	int
);	