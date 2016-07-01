"""This is the main server module for the bad movie science web app"""

import bleach
import json
import psycopg2
import random
import string

from oauth2client import client, crypt

from flask import Flask, jsonify, render_template, request, session

APP = Flask(__name__, static_folder='static', static_url_path='')
CLIENT_ID = ("514418218462-4g3jcfq7dnpaorj2bls6n9enm9nmf9g2" +
             ".apps.googleusercontent.com")

APP.secret_key = 'for SC13NC3! Hahahaha!'


def connect():
    """Returns a database connection."""
    return psycopg2.connect("dbname=catalogdb")


def check_user(token):
    try:
        idinfo = client.verify_id_token(token, CLIENT_ID)
        return True
    except crypt.AppIdentityError as e:
        print e
        return False


def check_session(state, token):
    if check_user(token) and (session['state'] == state):
        return True
    else:
        return False


class DB(object):
    """Functions used to interact with a psql database"""

    def __init__(self, db_con_str="dbname=catalogdb"):
        """Connect to database upon initialization"""
        self.conn = psycopg2.connect(db_con_str)

    def cursor(self):
        """Return the current cursor of the database"""
        return self.conn.cursor()

    @staticmethod
    def close(conn):
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

    def execute(self, query, close=True, **optional):
        """Connects to psql database and execute specified query"""
        # Create a cursor
        cur = self.cursor()
        # Execute sql -- the meat of the function
        if 'params' in optional:
            try:
                cur.execute(query, tuple(optional['params'],))
            except psycopg2.Error as e:
                print e
        else:
            cur.execute(query)
        # Define connection parameters
        parm = {"conn": self.conn, "cur": cur if not close else None}
        if close:
            # Make database changes persistent
            self.conn.commit()
            self.close(parm)
        # Return the connection and cursor to fetch rows
        return parm


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class Setup(object):
    """Methods used to populate the movie dabase with sample values if empty"""

    def __init__(self):
        pass

    @staticmethod
    def load_genres():
        """Loads sample genres into databse."""
        genres = ["Comedy", "Drama", "Non-fiction", "Realistic fiction",
                  "Action", "Romance", "Satire", "Tragedy", "Tragicomedy",
                  "Horror", "Sci-fi"]
        # Setup literary genres
        for value in genres:
            query = ("INSERT INTO genres (name) "
                     "VALUES(%s);")
            DB().execute(query, params=bleach.clean(value))

    @staticmethod
    def load_movies():
        """Loads sample movies into databse."""
        # Setup Movies
        movies = {
            "The Meowtian": "Sci-fi",
            "JigPaw": "Horror",
            "Captain Meowica": "Action",
            "Young Purrinstein": "Comedy",
            "Catsablanca": "Romance"
        }
        for key in movies:
            # Find corresponding index in genres.
            # Psql may not match row number with index in GENRES list.
            query = ("SELECT id FROM genres "
                     "WHERE name = %s;")
            conn = DB().execute(query, False, params=bleach.clean(movies))
            index = conn["cur"].fetchone()[0]
            DB().close(conn)
            movies[key] = index
            # Insert movies into database
            query = ("INSERT INTO movies (title, genre) "
                     "VALUES(%s, %s);")
            conn = DB().execute(query, params=[bleach.clean(key), movies[key]])

    @staticmethod
    def load_sciences():
        """Loads sample science fields into database."""
        # Set up science fields
        fields = {
            "Physics": "The study of matter and motion.",
            "Chemistry": "The study of matter and its structural changes.",
            "Earth Science": "The study of the planet Earth.",
            "Ecology": "The study of organisms and their relationship with their environment.",
            "Oceanography": "The study of oceans.",
            "Geology": "The study of rocks and how they change.",
            "Meteorology": "The study of atmospheres.",
            "Zoology": "The study of animal kingdoms.",
            "Human Biology": "The study of human anatomy and physiology.",
            "Botany": "The study of plants.",
            "Social Science": "The study of societies.",
            "Logic": "The study of inference and correct reasoning.",
            "Mathematics": "The study of patterns and conjectures independent of experience.",
            "Statistics": "The study of collecting and interpretting data.",
            "Computer Science": "The study of the mathematics of computing."
        }
        for key in fields:
            query = ("INSERT INTO science (field, description) "
                     "VALUES(%s, %s);")
            DB().execute(query, params=[bleach.clean(key), bleach.clean(fields[key])])

    @staticmethod
    def get_db_state():
        """Checks to see if there are anything in the database tables. If not,
        loads samples."""
        # Check if Science and genre fields have anything in them.
        # Assume database is full
        databases = {
            "science": False,
            "genres": False,
            "movies": False
        }
        for table in databases:
            query = ("SELECT CASE "
                     "  WHEN EXISTS (SELECT * FROM %s LIMIT 1) THEN 1 "
                     "  ELSE 0 "
                     "END;" % (table))
            conn = DB().execute(query, False)
            rows = conn["cur"].fetchone()[0]
            DB().close(conn)
            if not rows:
                databases[table] = True
        return databases


class Comment(object):
    """Comment properties from psql catalog database"""

    # Setup schema for comment view
    schema = {"id": 0,
              "author": 1,
              "movie_id": 2,
              "movie_name": 3,
              "science_id": 4,
              "science": 5,
              "description": 6}

    def __init__(self):
        pass

    @staticmethod
    def get_comments(**optional):
        """Returns comments from content table Dynamically changes query based on
        optional parameters."""
        query = ("SELECT id, author, movie_id, movie_name, science_id, "
                 "science, description "
                 "FROM view_content "
                 "WHERE true ")
        if 'params' in optional:
            params = optional['params']
            filters = []
        if 'id' in params:
            query += ("AND id = %s ")
            filters.append(params['id'])
        if 'author' in params:
            query += ("AND author = %s ")
            filters.append(params['author'])
        if 'movie_id' in params:
            query += ("AND movie_id = %s ")
            filters.append(params['movie_id'])
        if 'science_id' in params:
            query += ("AND science_id = %s ")
            filters.append(params['science_id'])
        query += ";"
        conn = DB().execute(query, False, params=filters)
        comment = conn["cur"].fetchall()
        DB().close(conn)
        return comment


@APP.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@APP.route('/')
def render():
    """Renders the home page for the app."""
    return render_template('index.html')


@APP.route('/deleteComment', methods=['DELETE'])
def delete_comment():
    """Deletes comment from content table."""
    data = json.loads(request.data)
    if check_session(data['stateid'], data['token']):
        query = ("DELETE FROM content WHERE id = %s;")
        DB().execute(query, params=[data['id']])
        # Make sure comment was submitted to database
        return json.dumps({
            'result': 'ok'
        })
    else:
        raise InvalidUsage('User not validated.', status_code=410)


@APP.route('/getComments', methods=['POST'])
def get_comments():
    """Returns comment from content table."""
    # Setup comment paramaters
    data = json.loads(request.data)['params']
    commdb = Comment()
    result = commdb.get_comments(params=data)
    return json.dumps({'comment': result,
                       'schema': commdb.schema})


@APP.route('/getAppInit', methods=['GET'])
def get_hierarchy():
    """Creates the sidenav heirarchy for naviation."""
    # Set up genres query
    query = ("SELECT id, name FROM genres ORDER BY name;")
    # Execute query
    conn = DB().execute(query, False)
    # Define output
    genres = conn["cur"].fetchall()
    DB().close(conn)

    # Set Up science query
    query = ("SELECT id, field FROM science ORDER BY field;")
    # Execute query
    conn = DB().execute(query, False)
    # Define output
    fields = conn["cur"].fetchall()
    DB().close(conn)

    return json.dumps({
        'genres': genres,
        'fields': fields
    })


@APP.route('/getGenres', methods=['POST'])
def get_genres():
    """Gets genres from genre fields."""
    data = json.loads(request.data)['id']
    # Set up movies query
    query = ("SELECT id, name, description FROM genres ")
    if data is not None:
        query += ("WHERE id = %s ")
    query += ("ORDER BY name;")
    # Execute query
    conn = DB().execute(query, False, params=[data])
    # Define output
    genres = conn["cur"].fetchall()
    DB().close(conn)

    return json.dumps({
        'genres': genres,
        'schema': {
            'id': 0,
            'name': 1,
            'description': 2
        }
    })


@APP.route('/getGenreMovies', methods=['POST'])
def get_genre_movies():
    """If genre id is passed, returns all movies with a specific gnere."""
    # I know there's a more efficient way to do this by combining it with
    # getMovies
    data = json.loads(request.data)['id']
    # Set up movies query
    query = ("SELECT id, title, genre FROM movies ")
    if data is not None:
        query += ("WHERE genre = %s ")
    query += ("ORDER BY title;")
    # Execute query
    conn = DB().execute(query, False, params=[data])
    # Define output
    movies = conn["cur"].fetchall()
    DB().close(conn)

    return json.dumps({
        'movies': movies,
        'schema': {
            'id': 0,
            'title': 1,
            'genre': 2
        }
    })


@APP.route('/getMovies', methods=['POST'])
def get_movies():
    """Returns all or one movie from movies database."""
    data = json.loads(request.data)['id']
    # Set up movies query
    query = ("SELECT id, title, genre FROM movies ")
    if data is not None:
        query += ("WHERE id = %s ")
    query += ("ORDER BY title;")
    # Execute query
    conn = DB().execute(query, False, params=[data])
    # Define output
    movies = conn["cur"].fetchall()
    DB().close(conn)

    return json.dumps({
        'movies': movies,
        'schema': {
            'id': 0,
            'title': 1,
            'genre': 2
        }
    })


@APP.route('/getRandomPage', methods=['POST'])
def get_random_page():
    """Finds a random id from a table called specified by the front-end."""
    data = bleach.clean(json.loads(request.data)['table'])
    # Set up movies query
    query = ("SELECT id FROM %s OFFSET FLOOR(RANDOM() * "
             "(SELECT COUNT(id) FROM %s)) LIMIT 1 ;" % (data, data))
    # Execute query
    conn = DB().execute(query, False)
    # Define output
    page_id = conn["cur"].fetchone()[0]
    DB().close(conn)

    return json.dumps({'id': page_id})


@APP.route('/getScience', methods=['POST'])
def get_science():
    """Gets all or one science field from database."""
    # Set up movies query
    query = ("SELECT id, field, description FROM science ")
    try:
        data = json.loads(request.data)['id']
        query += ("WHERE id = %s ORDER BY field;")
        conn = DB().execute(query, False, params=[data])
    except:
        query += ("ORDER BY field;")
        print query
        conn = DB().execute(query, False)
    print query
    # Define output
    science = conn["cur"].fetchall()
    DB().close(conn)

    return json.dumps({
        'science': science,
        'schema': {
            'id': 0,
            'field': 1,
            'description': 2
        }
    })


@APP.route('/getUser', methods=['POST'])
def get_user():
    """If user isn't in database, add them. Return id."""
    data = json.loads(request.data)
    if ('token' in data) and check_user(data['token']):
        user_email = data['user']
        state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                        for x in xrange(32))
        session['state'] = state
        # Set up movie query
        query = ("SELECT id "
                 "FROM users "
                 "WHERE email = %s;")
        # Execute query
        conn = DB().execute(query, False, params=[bleach.clean(user_email)])
        # Define output
        user_param = conn["cur"].fetchone()
        DB().close(conn)
        # If user not in database, add them
        if user_param is None:
            # Set up query
            query2 = ("INSERT INTO users (email) "
                      "VALUES(%s);")
            conn = DB().execute(query2, True,
                                params=[bleach.clean(user_email)])
            # Rerun initial query to find new id
            conn = DB().execute(query, False,
                                params=[bleach.clean(user_email)])
            user_param = conn["cur"].fetchone()
            DB().close(conn)
        return json.dumps({'id': user_param[0], 'csrf': state})
    else:
        raise InvalidUsage('User not validated.', status_code=410)


@APP.route('/postComment', methods=['POST'])
def post_comment():
    """Add user generated comment to content table."""
    data = json.loads(request.data)
    if check_session(data['stateid'], data['token']):
        params_submit = ([data['author'], data['movie'], data['science'],
                          bleach.clean(data['description'])])
        query = ("INSERT INTO content (author, movie, science, description) "
                 "VALUES(%s, %s, %s, %s) "
                 "RETURNING id;")
        conn = DB().execute(query, False, params=params_submit)
        comment_id = conn["cur"].fetchone()[0]
        DB().close(conn)
        # Make sure comment was submitted to database
        params = {'id': comment_id}
        check_submit = Comment()
        result = check_submit.get_comments(params=params)[0]
        return json.dumps({
            'comment': result,
            'schema': check_submit.schema
        })
    else:
        raise InvalidUsage('User not validated.', status_code=410)


@APP.route('/searchMovies', methods=['POST'])
def search_movies():
    """For md-autocomplete Search movie by title."""
    data = json.loads(request.data)['query']
    # Set up genres query
    query = ("SELECT id, title, genre FROM movies "
             "WHERE title ILIKE CONCAT('%%',%s,'%%') ORDER BY title LIMIT 10;")
    # Execute query
    conn = DB().execute(query, False, params=[bleach.clean(data)])
    # Define output
    movies = conn["cur"].fetchall()
    DB().close(conn)
    return json.dumps({
        'movies': movies,
        'schema': {
            'id': 0,
            'title': 1,
            'genre': 2
        }
    })


@APP.route('/updateComment', methods=['PUT'])
def update_comment():
    """Allow user to update their own comment."""
    data = json.loads(request.data)
    if check_session(data['stateid'], data['token']):
        params = ([data['author'], data['movie'], data['science'],
                  bleach.clean(data['description']), data['id']])
        query = ("UPDATE content "
                 "SET author = %s, movie = %s, science = %s, description = %s "
                 "WHERE id = %s;")
        DB().execute(query, True, params=params)
        # Make sure comment was submitted to database
        return json.dumps({
            'result': 'ok'
        })
    else:
        raise InvalidUsage('User not validated.', status_code=410)


if __name__ == '__main__':
    SETUP = Setup()
    DATABASE = SETUP.get_db_state()
    if DATABASE["genres"]:
        SETUP.load_genres()
    if DATABASE["movies"]:
        SETUP.load_movies()
    if DATABASE["science"]:
        SETUP.load_sciences()
    APP.run(host='0.0.0.0', port=8080)
