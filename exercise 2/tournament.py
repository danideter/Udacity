#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


class DB:

    def __init__(self, db_con_str="dbname=tournament"):
        """Connect to database upon initialization"""
        self.conn = psycopg2.connect(db_con_str)

    def cursor(self):
        """Return the current cursor of the database"""
        return self.conn.cursor();

    def close(self, conn):
        """Closes the current database connection

        Args:
          conn: the dictionary returned from BD().execute(). It should contain
          a conn and cursor. If there is no current cursor, it should equal
          None"""
        # Close cursor
        if conn["cur"] != None:
            # Make database changes persistent and close cursor
            conn["conn"].commit()
            conn["cur"].close()
        # Close databaae
        conn["conn"].close()

    def execute(self, query, close=True):
        # Create a cursor
        cur = self.cursor()
        # Execute sql -- the meat of the function
        cur.execute(query)
        # Define connection parameters
        parm = {"conn": self.conn, "cur": cur if not close else None}
        if close:
            # Make database changes persistent
            self.conn.commit()
            self.close(parm)
        # Return the connection and cursor to fetch rows
        return parm


def deleteMatches():
    """Remove all the match records from the database."""
    # Set up query
    query = ("DELETE "
            "FROM matches; ")
    # Execute query
    DB().execute(query)


def deletePlayers():
    """Remove all the player records from the database."""
    # Set up query
    query = ("DELETE "
            "FROM players; ")
    # Execute query
    DB().execute(query)
    

def countPlayers():
    """Returns the number of players currently registered."""
    # Set up query
    query = ("SELECT COUNT(id) "
            "FROM players; ")
    # Execute query and keep connection open
    conn = DB().execute(query, False)
    # Define output
    count = conn["cur"].fetchone()[0]
    # Close databaae
    DB().close(conn)
    # Returns a row from the query as a python object
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    # Set up query
    query = ("INSERT INTO players (name) "
             "VALUES('%s');" % (name.replace("'","''")))
    # Execute query
    DB().execute(query)


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
    # Set up query
    query = ("SELECT * "
             "FROM standings ")
    # Execute query
    conn = DB().execute(query, False)
    # Define output
    out = conn["cur"].fetchall()
    # Close databaae
    DB().close(conn)
    # Returns standings
    return out


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # Set up query
    query = ("INSERT INTO matches (winner, loser) "
             "VALUES(%d, %d);" % (winner, loser))
    # Execute query
    DB().execute(query)
 
 
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
    # Set up query
    query = ("SELECT * "
             "FROM pairings ")
    # Execute query
    conn = DB().execute(query, False)
    # Define output
    out = conn["cur"].fetchall()
    # Close databaae
    DB().close(conn)
    # Returns pairings
    return out

