'''
Created on Apr 30, 2018

@author: Piyawat Pemwattana
'''

class movieServiceRepository(object):

    def __init__(self, movieId, title, genres, fileImage):
        self.movieId = movieId
        self.title = title
        self.genres = genres
        self.fileImage = fileImage

    def get_file_image(self):
        return self.__fileImage


    def set_file_image(self, value):
        self.__fileImage = value


    def del_file_image(self):
        del self.__fileImage


    def get_movie_id(self):
        return self.__movieId


    def get_title(self):
        return self.__title


    def get_genres(self):
        return self.__genres


    def set_movie_id(self, value):
        self.__movieId = value


    def set_title(self, value):
        self.__title = value


    def set_genres(self, value):
        self.__genres = value


    def del_movie_id(self):
        del self.__movieId


    def del_title(self):
        del self.__title


    def del_genres(self):
        del self.__genres
    
    
        

    movieId = property(get_movie_id, set_movie_id, del_movie_id, "movieId's docstring")
    title = property(get_title, set_title, del_title, "title's docstring")
    genres = property(get_genres, set_genres, del_genres, "genres's docstring")
    fileImage = property(get_file_image, set_file_image, del_file_image, "fileImage's docstring")
    
    def to_JSON(self):
        return {
            'movieId' : self.movieId,
            'title' : self.title,
            'genres' : self.genres,
            'fileImage' : self.fileImage
        }
    