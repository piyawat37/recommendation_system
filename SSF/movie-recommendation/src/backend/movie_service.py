'''
Created on Dec 11, 2017

@author: Piyawat Pemwattana
'''
#Defined Version

from connectMongoDB import _connect_mongo
import numpy as np
import pandas as pd
from SystemConstant import SystemConstant
from pandas import json


def pom_version():
    pom = {
        'service' : 'movie-service',
        'version' : '0.0.1-PRODUCTION',
        'poc_version' : '0.0.6-PROTOTYPE',
        'create_date' : 'Created on Mar 3, 2018',
        'author' : 'Piyawat Pemwattana'
    }
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
def recommend_movies(predictions_df, userID, movies_df, original_ratings_df, num_recommendations=SystemConstant.RANGE_OF_PREDICTION):
    
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
    recommendations = (movies_df[~movies_df['movieId'].isin(user_full['movieId'])].
         merge(pd.DataFrame(sorted_user_predictions).reset_index(), how = 'left',
               left_on = 'movieId',
               right_on = 'movieId').
         rename(columns = {user_row_number: 'Predictions'}).
         sort_values('Predictions', ascending = False).
                       iloc[:num_recommendations, :-1]
                      )
    rec_movie_id_list = recommendations['movieId'].iloc[:SystemConstant.RANGE_OF_CATEGORY].tolist()
    

#     return user_full, recommendations
    return rec_movie_id_list, recommendations


def get_movies_classify_by_prediction(genres, predic, range):
    #TODO: Function classify genres by predic AUTHOR: PIYAWAT PEMWATTANA
    movie_list_filter_genres = predic.loc[predic['genres'].str.contains(genres)].iloc[:range]
    return movie_list_filter_genres

def transform_dataFrame(id):
    if id != None:
        movieServiceObj = {}
        ratings_df = initial_dataframe(collection='ratings')
        movies_df = initial_dataframe(collection='movies')
        movies_df.drop(movies_df.index[:1], inplace=True)
        movies_df['movieId'] = movies_df['movieId'].apply(pd.to_numeric)
        ratings_df['movieId'] = ratings_df['movieId'].apply(pd.to_numeric)
        ratings_df['rating'] = ratings_df['rating'].apply(pd.to_numeric)
    
        R_df = ratings_df.pivot(index = 'userId', columns ='movieId', values = 'rating').fillna(0)
        
        R = R_df.as_matrix()
        user_ratings_mean = np.mean(R, axis = 1)
        R_demeaned = R - user_ratings_mean.reshape(-1, 1)
        
        from scipy.sparse.linalg import svds
        U, sigma, Vt = svds(R_demeaned, k = 2)
        
        sigma = np.diag(sigma)
        
        all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
        preds_df = pd.DataFrame(all_user_predicted_ratings, columns = R_df.columns)
            
        recommended_list, recommendations = recommend_movies(preds_df, id, movies_df, ratings_df)
        movieServiceObj['recommended'] = recommended_list
        if len(recommendations) > 0 :
            for value in SystemConstant.GENRES:
                movie_list_filter_genres = get_movies_classify_by_prediction(value, recommendations, SystemConstant.RANGE_OF_CATEGORY)
                if(len(movie_list_filter_genres) > 9):
                    movieServiceObj[value] = movie_list_filter_genres['movieId'].tolist()
    else:
        #Another Function DEF PLEASE LOGIN
        return "id none"
    
    return movieServiceObj
