#!/usr/bin/env python
# 
# catalog.py
#

import psycopg2
from flask import Flask
from flask import render_template

app = Flask(__name__, static_folder='static', static_url_path='')

def connect():
    """Returns a database connection."""
    return psycopg2.connect("dbname=catalog")


class DB:

    def __init__(self, db_con_str="dbname=catalog"):
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

"""		
# Only has movie, need to add genre and comments
@app.route('/movie/<int:movieID>')
def getMoviePage(movieID):
	# Set up movie query
	query = ("SELECT title, poster "
				"FROM movie "
				"WHERE id = %d" % movieID)
	# Execute query
	conn = DB().execute(query, False)
	# Define output
	title = conn["cur"].fetchone()
	# Set up genres
	query = ("SELECT name "
				"FROM genre "
				"WHERE movie_id = %d" % movieID)
	conn = DB().execute(query, False)
	genres = conn["cur"].fetchall()
	# Get comments
	query = ("SELECT flaw, description "
             "FROM content "
			 "WHERE movie_id = %d" % movieID)
	conn = DB().execute(query, False)
	genres = conn["cur"].fetchall()
	# Close database
	DB().close(conn)
	# Returns standings
	return title
	"""

@app.route('/')
def sup():
	print 1
	# return "Shoot da zombies in da head. Press A!"
	return render_template('index.html')

if __name__ == '__main__':
	print 2
	app.run(host='0.0.0.0', port=8080)