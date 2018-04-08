'''
Created on Apr 7, 2018

@author: Piyawat Pemwattana
'''

class SystemConstant:
    RANGE_OF_PREDICTION = 200;
    RANGE_OF_CATEGORY = 10;
    GENRES = ['Adventure',
                'Animation',
#                 'Children',
                'Comedy',
                'Fantasy',
                'Romance',
                'Drama',
                'Crime',
                'Thriller',
                'Horror',
                "Sci-Fi",
                'Mystery',
#                 'Documentary',
                'War',
                'Action',
#                 'Western',
                'Musical'
#                 'Film-Noir' 
                ]
    
    
    #Example
    def DEFINED_GENRES(self, genres):
        if genres == 'Adventure':
            return 1
        elif genres == 'Animation':
            return 2
        