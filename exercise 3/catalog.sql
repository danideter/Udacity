--sql for badmoviescience

DROP DATABASE IF EXISTS catalogdb;
CREATE DATABASE catalogdb;
\c catalogdb; 

CREATE TABLE users (
	id	SERIAL PRIMARY KEY,
	email VARCHAR NOT NULL
);

CREATE TABLE genres (
	id	SERIAL PRIMARY KEY,
	name VARCHAR NOT NULL,
	description VARCHAR
);

CREATE TABLE movies (
	id	SERIAL PRIMARY KEY,
	title VARCHAR NOT NULL,
	genre INT REFERENCES genres(id),
	poster VARCHAR
);

CREATE TABLE science (
	id	SERIAL PRIMARY KEY,
	field VARCHAR NOT NULL,
	description VARCHAR NOT NULL,
	image VARCHAR
);

CREATE TABLE content (
	id	SERIAL PRIMARY KEY,
	author INT REFERENCES users(id),
	movie INT REFERENCES movies(id),
	science INT REFERENCES science(id),
	description VARCHAR NOT NULL
);

CREATE VIEW view_content AS
	SELECT 
		c.id AS id,
		c.author AS author,
		c.movie AS movie_id,
		m.title AS movie_name,
		c.science AS science_id,
		s.field AS science,
		c.description AS description
	FROM content AS c
	INNER JOIN movies AS m
	ON c.movie = m.id
	INNER JOIN science AS s
	ON c.science = s.id
	ORDER BY c.id;
	
