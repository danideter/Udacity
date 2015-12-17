#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    # Create connection to database
    conn = connect()
    cur = conn.cursor()
    # Execute sql -- the meat of the function
    cur.execute("DELETE "
                "FROM matches;")
    # Make database changes persistent
    conn.commit()
    # Close databaae
    cur.close()
    conn.close()
    


def deletePlayers():
    """Remove all the player records from the database."""
    # Create connection to database
    conn = connect()
    cur = conn.cursor()
    # Execute sql -- the meat of the function
    cur.execute("DELETE "
                "FROM players; ")
    # Make database changes persistent
    conn.commit()
    # Close databaae
    cur.close()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    # Execute sql -- the meat of the function
    cur.execute("SELECT COUNT(id) "
                "FROM players; ")
    # Define output
    count = cur.fetchone()[0]
    # Close databaae
    cur.close()
    conn.close()
    # Returns a row from the query as a python object
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    # Create connection to database
    conn = connect()
    cur = conn.cursor()
    # Execute sql -- the meat of the function
    name = name.replace("'","''")
    cur.execute("INSERT INTO players (name) "
                "VALUES('" + name + "');")
    # Make database changes persistent
    conn.commit()
    # Close databaae
    cur.close()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    # Create connection to database
    conn = connect()
    cur = conn.cursor()
    # Execute sql -- the meat of the function
    # Is there a more elegant solution besides two joins
    cur.execute("SELECT "
                "  p.id AS id, "
                "  p.name AS name, "
                "  CASE WHEN w.wins IS NULL THEN 0 ELSE w.wins END AS wins, "
                # Combines wins and losses to find mathes played
                "  CASE WHEN l.losses IS NULL THEN 0 ELSE l.losses END + "
                "  CASE WHEN w.wins IS NULL THEN 0 ELSE w.wins END AS rounds "
                "FROM "
                "  (SELECT id, name "
                "  FROM players) AS p "
                # Find player's wins and join on id
                "LEFT JOIN "
                "  (SELECT winner, COUNT(winner) AS wins "
                "  FROM matches "
                "  GROUP BY winner ) AS w "
                "ON w.winner = p.id "
                # Find player's losses and join on id
                "LEFT JOIN "
                "  (SELECT loser, COUNT(loser) AS losses "
                "  FROM matches "
                "  GROUP BY loser ) AS l "
                "ON l.loser = p.id "
                "ORDER BY wins; ")
    # Make database changes persistent
    conn.commit()
    # Define output
    out = cur.fetchall()
    # Close databaae
    cur.close()
    conn.close()
    # Returns a row from the query as a python object
    return out


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # Create connection to database
    conn = connect()
    cur = conn.cursor()
    # Execute sql -- the meat of the function
    cur.execute("INSERT INTO matches (winner, loser) "
                "VALUES(" + str(winner) + ", " + str(loser) + ");")
    # Make database changes persistent
    conn.commit()
    # Close databaae
    cur.close()
    conn.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # Create connection to database
    conn = connect()
    cur = conn.cursor()
    # Execute sql -- the meat of the function
    cur.execute("SELECT a.id, a.name, b.id, b.name "
                # Find position based on wins
                "FROM "
                "  (SELECT p.id AS id, p.name AS name, "
                "  CASE WHEN w.wins IS NULL THEN 0 ELSE w.wins END AS wins, "
                "  row_number() OVER (ORDER BY wins DESC) AS position "
                "  FROM "
                "    (SELECT id, name "
                "    FROM players) AS p "
                # Find player's wins and join on id
                "  LEFT JOIN "
                "    (SELECT winner, COUNT(winner) AS wins "
                "    FROM matches "
                "  GROUP BY winner ) AS w "
                "  ON w.winner = p.id) AS a "
                # Join on self, but with position - 1
                # Tried looking up macros in psql, but couldn't find much
                # documentation for script expansion?
                "INNER JOIN "
                "  (SELECT p.id AS id, p.name AS name, "
                "  CASE WHEN w.wins IS NULL THEN 0 ELSE w.wins END AS wins, "
                "  row_number() OVER (ORDER BY wins DESC) - 1 AS position "
                "  FROM "
                "    (SELECT id, name "
                "    FROM players) AS p "
                # Find player's wins and join on id
                "  LEFT JOIN "
                "    (SELECT winner, COUNT(winner) AS wins "
                "    FROM matches "
                "  GROUP BY winner ) AS w "
                "  ON w.winner = p.id) AS b "
                "ON a.position = b.position "
                # Eliminate even numbered positions to remove double bookings 
                "WHERE a.position % 2 != 0 ")
    # Make database changes persistent
    conn.commit()
    # Define output
    out = cur.fetchall()
    # Close databaae
    cur.close()
    conn.close()
    # Returns a row from the query as a python object
    return out


