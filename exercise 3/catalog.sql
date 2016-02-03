--sql for badmoviescience.net

DROP DATABASE IF EXISTS catalogdb;
CREATE DATABASE catalogdb;
\c catalogdb; 

CREATE TABLE users (
	id	SERIAL PRIMARY KEY,
	username 	VARCHAR NOT NULL
);

CREATE TABLE movie (
	id	SERIAL PRIMARY KEY,
	title VARCHAR NOT NULL,
	poster VARCHAR NOT NULL
);

CREATE TABLE genre (
	id	SERIAL PRIMARY KEY,
	movie_id INT REFERENCES movie(id),
	name VARCHAR NOT NULL,
	description VARCHAR NOT NULL
);

CREATE TABLE science (
	id	SERIAL PRIMARY KEY,
	field VARCHAR NOT NULL,
	description VARCHAR NOT NULL,
	image
);

CREATE TABLE content (
	id	SERIAL PRIMARY KEY,
	movie INT REFERENCES movie(id),
	flaw INT REFERENCES science(id),
	description VARCHAR NOT NULL
);

CREATE VIEW latest_content AS
	SELECT 
		c.id AS id,
		c.movie AS movie_id,
		m.name AS movie_name,
		c.flaw AS science_id,
		s.field AS science,
		c.description AS description
	FROM content AS c
	INNER JOIN movie AS m
	ON c.movie = m.id
	INNER JOIN science AS s
	ON c.flaw = s.id
	ORDER BY c.id
	LIMIT 5;