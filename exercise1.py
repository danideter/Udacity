import fresh_tomatoes

print "Fez is cool"

class movie():
    def __init__(self,title,trailer,poster):
        self.title = title
        self.trailer_youtube_url = trailer
        self.poster_image_url = poster

alien = movie("Alien","https://www.youtube.com/watch?v=LjLamj-b0I8","http://40.media.tumblr.com/bc63f2e52e1afc5b33d1c80e993e7fdf/tumblr_mnulojVUcd1qzcgluo1_1280.jpg")
aliens = movie("Aliens","https://www.youtube.com/watch?v=XKSQmYUaIyE","https://www.movieposter.com/posters/archive/main/174/MPW-87199")
alien3 = movie("Aliens3","https://www.youtube.com/watch?v=UVb4Y49L7_U","http://www.impawards.com/1992/posters/alien_three_ver2.jpg")

fresh_tomatoes.open_movies_page([alien, aliens, alien3])
