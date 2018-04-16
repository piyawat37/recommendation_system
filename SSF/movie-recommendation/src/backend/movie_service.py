'''
Created on Dec 11, 2017

@author: Piyawat Pemwattana
'''
#Defined Version

from notebook.tests.test_serverextensions import SimpleNamespace
from pandas import json

from SystemConstant import SystemConstant
from connectMongoDB import _connect_mongo
from recMovieDto import recMovieDto
from pomServiceDto import pomServiceDto
import numpy as np
import pandas as pd
from jsonschema._validators import items
from jedi.refactoring import rename
from sympy.physics.units.definitions import percent



def pom_version():
    pom = pomServiceDto('movie-service',
                  '0.0.1-PRODUCTION',
                  '0.0.8-PROTOTYPE',
                  'Created on Dec 11, 2018',
                  'Piyawat Pemwattana')
    return pom


db = _connect_mongo(host='localhost', port=27017, username=None, password=None, db='recommendation_system')

def initial_dataframe(collection, query={}, no_id=True):
    cursor = db[collection].find(query)
    df = pd.DataFrame(list(cursor))
    if no_id:
        del df['_id']
    return df

'''
   # Ref. Nick Becker, Data Scientist at Enigma Technologies
'''
def recommend_movies(predictions_df, userID, movies_df, original_ratings_df, users_df, num_recommendations=SystemConstant.RANGE_OF_PREDICTION):
    
    # Get and sort the user's predictions
    user_row_number = userID - 1 # UserID starts at 1, not 0
    sorted_user_predictions = predictions_df.iloc[user_row_number].sort_values(ascending=False)
    # Get the user's data and merge in the movie information.
    user_data = original_ratings_df[original_ratings_df.userId == str(userID)]
    user_full = (user_data.merge(movies_df, how = 'left', left_on = 'movieId', right_on = 'movieId').
                     sort_values(['rating'], ascending=False)
                 )

#     print('User {0} has already rated {1} movies.'.format(userID, user_full.shape[0]))
#     print('Recommending the highest {0} predicted ratings movies not already rated.'.format(num_recommendations))
    
    # Recommend the highest predicted rating movies that the user hasn't seen yet.
#     recommendations = (movies_df[~movies_df['movieId'].isin(user_full['movieId'])].
#          merge(pd.DataFrame(sorted_user_predictions).reset_index(), how = 'left',
#                left_on = 'movieId',
#                right_on = 'movieId').
#          rename(columns = {user_row_number: 'Predictions'}).
#          sort_values('Predictions', ascending = False)
#                       )
    
    predict_recommend = (movies_df[~movies_df['movieId'].isin(user_full['movieId'])]
                       .merge(pd.DataFrame(sorted_user_predictions).reset_index(), how = 'left',
                              left_on = 'movieId',
                              right_on = 'movieId').
                       rename(columns = {user_row_number: 'Predictions'})
                       .sort_values('Predictions', ascending = False))
#     percents = percent(recommendations['Predictions'])

#     print(recommendations)
#     return user_full, recommendations
    #Merge Rating
#     merge_ratings_user = pd.merge(original_ratings_df, users_df, on = 'userId')
#     rec_with_rating = pd.merge(predict_recommend, merge_ratings_user, how = 'left'
#                                , left_on = 'movieId', right_on='movieId').filter(items=['movieId', 'title', 'genres', 'username', 'Predictions', 'rating'])
#     recommendations = rec_with_rating.groupby(['movieId','title', 'genres', 'username'], as_index=False).mean().sort_values('Predictions', ascending = False).head(20)
    print(predict_recommend)
    return predict_recommend

def get_movies_top_rate(movies, users, ratings):
    merge_ratings_user = pd.merge(ratings,users, on = 'userId')
    movie_data = pd.merge(movies,merge_ratings_user, on = 'movieId').filter(items=['movieId', 'title', 'genres', 'rating'])
    movie_top_rate = movie_data.groupby(['movieId','title', 'genres'], as_index=False).mean().sort_values('rating', ascending = False).head(20)
    return movie_top_rate

def get_movies_classify_by_prediction(genres, predic, range):
    #TODO: Function classify genres by predic AUTHOR: PIYAWAT PEMWATTANA
    movie_list_filter_genres = predic.loc[predic['genres'].str.contains(genres)].iloc[:range]
    return movie_list_filter_genres

def transform_dataFrame(id=None):
    ratings_df = initial_dataframe(collection='ratings')
    movies_df = initial_dataframe(collection='movies')
    users_df = initial_dataframe(collection='users')
    movies_df['movieId'] = movies_df['movieId'].apply(pd.to_numeric)
    ratings_df['movieId'] = ratings_df['movieId'].apply(pd.to_numeric)
    ratings_df['rating'] = ratings_df['rating'].apply(pd.to_numeric)
    movie_list = []
    movieServiceObj = {}
    if id != None:
    
        R_df = ratings_df.pivot(index = 'userId', columns ='movieId', values = 'rating').fillna(0)
        
        R = R_df.as_matrix()
        user_ratings_mean = np.mean(R, axis = 1)
        R_demeaned = R - user_ratings_mean.reshape(-1, 1)
        
        from scipy.sparse.linalg import svds
        U, sigma, Vt = svds(R_demeaned, k = 1)
        
        sigma = np.diag(sigma)
        
        all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
        preds_df = pd.DataFrame(all_user_predicted_ratings, columns = R_df.columns)
            
        recommendations = recommend_movies(preds_df, id, movies_df, ratings_df, users_df)
        
        if len(recommendations) > 0 :
            for genres in SystemConstant.GENRES:
                movie_list = []
                movie_list_filter_genres = get_movies_classify_by_prediction(genres, recommendations, SystemConstant.RANGE_OF_CATEGORY)
                if(len(movie_list_filter_genres) > 17):
                    for index, row in movie_list_filter_genres.iterrows():
                        movieObj = recMovieDto(row['movieId'], row['title'], row['genres'])
#                         movieServiceObj[genres] = {
#                             movieObj.get_title() : movieObj
#                         }
                        movie_list.append(movieObj.toJSON())
#                         print(genres + ', ' +movieObj.get_title())
                if len(movie_list) > 0 :
                    movieServiceObj[genres] = movie_list
            
            for index, row in recommendations.iloc[:SystemConstant.RANGE_OF_CATEGORY].iterrows():
                movieObj = recMovieDto(row['movieId'], row['title'], row['genres'])
                movie_list.append(movieObj.toJSON())
            if len(movie_list) > 0 :
                movieServiceObj['Recommended'] = movie_list
        return movieServiceObj
    else:
        #Another Function DEF PLEASE LOGIN
        movies_top = get_movies_top_rate(movies_df, users_df, ratings_df)
        if len(movies_top) > 0 :
            movie_list = []
            for index, row in movies_top.iterrows():
                movieObj = recMovieDto(row['movieId'], row['title'], row['genres'], row['rating'])
                movie_list.append(movieObj.toJSON())
            
            movieServiceObj['movieTopRate'] = movie_list    
        return movieServiceObj

movies_top = transform_dataFrame(1)
# print(movies_top)