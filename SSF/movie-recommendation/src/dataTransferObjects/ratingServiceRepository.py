'''
Created on Apr 1, 2018

@author: Piyawat Pemwattana
'''

class ratingServiceRepository(object):

    def __init__(self, userId, movieId, rating, timestamp):
        self.userId = userId
        self.movieId = movieId
        self.rating = rating
        self.timestamp = timestamp

    def get_user_id(self):
        return self.__userId


    def get_movie_id(self):
        return self.__movieId


    def get_rating(self):
        return self.__rating


    def get_timestamp(self):
        return self.__timestamp


    def set_user_id(self, value):
        self.__userId = value


    def set_movie_id(self, value):
        self.__movieId = value


    def set_rating(self, value):
        self.__rating = value


    def set_timestamp(self, value):
        self.__timestamp = value


    def del_user_id(self):
        del self.__userId


    def del_movie_id(self):
        del self.__movieId


    def del_rating(self):
        del self.__rating


    def del_timestamp(self):
        del self.__timestamp

    userId = property(get_user_id, set_user_id, del_user_id, "userId's docstring")
    movieId = property(get_movie_id, set_movie_id, del_movie_id, "movieId's docstring")
    rating = property(get_rating, set_rating, del_rating, "rating's docstring")
    timestamp = property(get_timestamp, set_timestamp, del_timestamp, "timestamp's docstring")
    
    
    def to_JSON(self):
        return {
            'userId' : self.get_user_id(),
            'movieId' : self.get_movie_id(),
            'rating' : self.get_rating(),
            'timestamp' : self.get_timestamp()
        }
