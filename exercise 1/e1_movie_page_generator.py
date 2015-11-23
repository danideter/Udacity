""" This program passes movie attributes to fresh_tomatoes_mod in order to
generate a webpage about the Alien trilogy.

Attributes:
    alien (movie): the title, trailer, and poster of the first alien movie.
    aliens (movie): the title, trailer, and poster of the second alien movie.
    alien3 (movie): the title, trailer, and poster of the third alien movie.

Args:
    None.

Returns:
    None.

"""

import fresh_tomatoes_mod

# Create movie class to add movie properties as html in fresh_tomatos_mod
# Pylint suggests I used a dictionary instead? But the instructions say to make a
# movie class, so I'm going with that.
class Movie(object):
    """ This class creates a movie data atructure to be passed on to
    fres_tomatos_mod.

    Args:
        title (string): the title of the film.
        trailer (string): the url of a youtube trailor of the film.
        poster (string): the image url of a poster of this film.

    Returns:
        None.

"""
    def __init__(self, title, trailer, poster):
        self.title = title
        self.trailer_youtube_url = trailer
        self.poster_image_url = poster

# Create three instances to contain the best trology ever
ALIEN = Movie("Alien", "https://www.youtube.com/watch?v=LjLamj-b0I8",
              "http://40.media.tumblr.com/bc63f2e52e1afc5b33d1c80e993e7fdf/tumblr_mnulojVUcd1qzcgluo1_1280.jpg")
ALIENS = Movie("Aliens", "https://www.youtube.com/watch?v=XKSQmYUaIyE",
               "https://www.movieposter.com/posters/archive/main/174/MPW-87199")
ALIEN3 = Movie("Aliens3", "https://www.youtube.com/watch?v=UVb4Y49L7_U",
               "http://www.impawards.com/1992/posters/alien_three_ver2.jpg")

# Run a modded version of fresh_tomatos
fresh_tomatoes_mod.open_movies_page([ALIEN, ALIENS, ALIEN3])
