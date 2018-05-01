'''
Created on Dec 11, 2017

@author: Piyawat Pemwattana
'''
#Defined Version

from flask import Response
from numpy import delete
import pandas
import time

from QLearning import QLearningTable
from SystemConstant import SystemConstant
from SystemException import SystemException
from SystemMessage import SystemMessage
from connectMongoDB import _connect_mongo
from movieServiceRepository import movieServiceRepository
import numpy as np
import pandas as pd
from pomServiceDto import pomServiceDto
from ratingServiceRepository import ratingServiceRepository
from recMovieDto import recMovieDto
from user_service import data_test


def pom_version():
    pom = pomServiceDto('movie-service',
                  '1.0.1',
                  '0.0.11-PROTOTYPE',
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
    movie_data = original_ratings_df[original_ratings_df.userId == userID]
    user_full = (movie_data.merge(movies_df, how = 'left', left_on = 'movieId', right_on = 'movieId').
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
    return predict_recommend

def get_movies_top_rate(movies, users, ratings):
    merge_ratings_user = pd.merge(ratings,users, on = 'userId')
    movie_data = pd.merge(movies,merge_ratings_user, on = 'movieId').filter(items=['movieId', 'title', 'genres', 'rating'])
    movie_top_rate = movie_data.groupby(['movieId','title', 'genres'], as_index=False).mean().sort_values('rating', ascending = False)
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
    ranking = 0
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
        
#         QLearningTable.learn(s, a, r, s_)
        
        movies_top = get_movies_top_rate(movies_df, users_df, ratings_df)
        if len(movies_top) > 0 :
            movie_list = []
            for index, row in movies_top.iterrows():
                movieObj = recMovieDto(row['movieId'], row['title'], row['genres'], row['rating'])
                movie_list.append(movieObj.toJSON())
            
            movieServiceObj['movieTopRate'] = movie_list
               
        if len(recommendations) > 0 :
            movie_list = []
            for index, row in recommendations.iloc[:SystemConstant.RANGE_OF_CATEGORY].iterrows():
                movieObj = recMovieDto(row['movieId'], row['title'], row['genres'])
                movie_list.append(movieObj.toJSON())
            if len(movie_list) > 0 :
                movieServiceObj['Recommended'] = movie_list
                
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
        for genres in SystemConstant.GENRES:
                movie_list = []
                movie_list_filter_genres = get_movies_classify_by_prediction(genres, movies_top, SystemConstant.RANGE_OF_CATEGORY)
                if(len(movie_list_filter_genres) > 17):
                    for index, row in movie_list_filter_genres.iterrows():
                        movieObj = recMovieDto(row['movieId'], row['title'], row['genres'])
                        movie_list.append(movieObj.toJSON())
                if len(movie_list) > 0 :
                    movieServiceObj[genres] = movie_list    
        return movieServiceObj

def get_all_movie():
    movies = db['movies']
    movieList = []
    cursor = movies.find({})
    for value in cursor:
        movieDto = recMovieDto(movieId=value['movieId'],title=value['title'],genres=value['genres'])
        movieList.append(movieDto.to_JSON_DataTable())
    return movieList

def update_movie(movieContext):
    db['movies'].find_one_and_update({'movieId':movieContext['movieId']}, {'$set': {'title': movieContext['title'], 'genres': movieContext['genres']}})
    movie = db['movies'].find_one({'movieId' : movieContext['movieId']})
    movieObjDto = recMovieDto(movieId=movie['movieId']
                              , title=movie['title']
                              , genres=movie['genres']
                              , rating=None)
    return movieObjDto

def add_rating(ratedContext):
    user = db['users'].find_one({'token' : ratedContext['token']})
    user_has_rated = db['ratings'].find_one({'userId' : user['userId'], 'movieId' : ratedContext['movieId']})
    if user_has_rated != None:
        db['ratings'].find_one_and_update({'userId':user['userId'], 'movieId' : ratedContext['movieId']}, {'$set': {'rating': str(ratedContext['rating'])}})
    else:
        ratingObj = ratingServiceRepository(userId=user['userId']
                                            , movieId=ratedContext['movieId']
                                            , rating=str(ratedContext['rating'])
                                            , timestamp="%d " %  time.time())
        db.ratings.insert_one(ratingObj.to_JSON())
    
    return user

def delete_movie(movieId):
    db.movies.delete_one({'movieId':movieId})

def check_duplicate_movie(title=None, movieId=None, language=None):
    isDuplicate = False
    movieObj = db['movies'].find_one({'title' : title})
    if movieId != None:
        if movieObj != None and movieObj['movieId'] != movieId:
            try:
                raise SystemException(SystemException.message_duplicate_context(None, SystemMessage.Msg['titleException-'+language], language))
            except SystemException as error:
                resp = Response({SystemException.message_duplicate_context(None, SystemMessage.Msg['titleException-'+language], language)}, status=400, mimetype='application/json')
                return resp
    else:
        if movieObj != None:
            try:
                raise SystemException(SystemException.message_duplicate_context(None, SystemMessage.Msg['titleException-'+language], language))
            except SystemException as error:
                resp = Response({SystemException.message_duplicate_context(None, SystemMessage.Msg['titleException-'+language], language)}, status=400, mimetype='application/json')
                return resp
            
    return isDuplicate
        

def create_new_movie(movie_data):
    print(movie_data['title'])
    print(movie_data['language'])
    if check_duplicate_movie(title=movie_data['title'],language=movie_data['language']) == False:
        movieGetMax = db.movies.find().sort('movieId', -1).limit(1)
        movieId = ''
        for cursor in movieGetMax:
            movieId = int(cursor['movieId'])+1
        movieObjRepo = movieServiceRepository(movieId=movieId, title=movie_data['title'], genres=movie_data['genres'])
        db.movies.insert_one(movieObjRepo.to_JSON())
        movieObj = db['movies'].find_one({'movieId' : movieId})
        print(movieObj)
        movieServiceObj = recMovieDto(movieId=movieObj['movieId'], title=movieObj['title'], genres=movieObj['genres'], rating=None)
        return movieServiceObj
    else:
        return check_duplicate_movie(title=movie_data['title'],language=movie_data['language'])

def data_test():
    return{
        'title':'sssssssss',
        'language' :'EN',
        'genres':'test|test'
    }

# print(create_new_movie(data_test()))
# movies_top = transform_dataFrame(6)
# print(movies_top)