'''
Created on Apr 1, 2018

@author: Piyawat Pemwattana
'''
import json


class recMovieDto(object):


    def __init__(self=None, movieId=None, title=None, genres=None, rating=None):
        self.movieId = movieId
        self.title = title
        self.genres = genres
        self.rating = rating

    def get_movie_id(self):
        return self.__movieId


    def get_title(self):
        return self.__title


    def get_genres(self):
        return self.__genres


    def get_rating(self):
        return self.__rating

    def set_movie_id(self, value):
        self.__movieId = value


    def set_title(self, value):
        self.__title = value


    def set_genres(self, value):
        self.__genres = value


    def set_rating(self, value):
        self.__rating = value

    def del_movie_id(self):
        del self.__movieId


    def del_title(self):
        del self.__title


    def del_genres(self):
        del self.__genres


    def del_rating(self):
        del self.__rating

    def toJSON(self):
        return {
            'movieId': self.movieId,
            'title': self.title,
            'genres': self.genres,
            'rating' : self.rating,
        }
    
    def to_JSON_DataTable(self):
        return {
            'movieId': self.movieId,
            'title': self.title,
            'genres': self.genres,
        } 
    
    def to_JSON_Update(self):
        return {
            'movieId': self.movieId,
            'title': self.title,
            'genres': self.genres,
        } 
        
    movieId = property(get_movie_id, set_movie_id, del_movie_id, "movieId's docstring")
    title = property(get_title, set_title, del_title, "title's docstring")
    genres = property(get_genres, set_genres, del_genres, "genres's docstring")
    rating = property(get_rating, set_rating, del_rating, "rating's docstring")
