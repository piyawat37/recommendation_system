'''
Created on Mar 3, 2018

@author: Piyawat Pemwattana
'''

'''
Created on Dec 11, 2017

@author: Piyawat Pemwattana
'''

import pandas as pd
import numpy as np
import absPath
from connectMongoDB import _connect_mongo
from pymongo import cursor

def initial_dataframe(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)
    cursor = db[collection].find(query)
    df = pd.DataFrame(list(cursor))
    if no_id:
        del df['_id']
    return df
        
ratings_df = initial_dataframe(db='recommendation_system', collection='ratings')
users_df = initial_dataframe(db='recommendation_system', collection='users')
movies_df = initial_dataframe(db='recommendation_system', collection='movies')
print(ratings_df)

# ratings_df.loc[0] = [1, 5377, 5, 1206759144]  # adding a row
# ratings_df.index = ratings_df.index + 1  # shifting index
# ratings_df = ratings_df.sort_index()  # sorting by index
# print(ratings_df)
print("----------------------------------------------------")
movies_df.drop(movies_df.index[:1], inplace=True)
movies_df['movieId'] = movies_df['movieId'].apply(pd.to_numeric)
ratings_df['movieId'] = ratings_df['movieId'].apply(pd.to_numeric)
# ratings_df['userId'] = ratings_df['userId'].apply(pd.to_numeric)
ratings_df['rating'] = ratings_df['rating'].apply(pd.to_numeric)
   
print(ratings_df.dtypes)

print(movies_df.head())
print(ratings_df.head())
R_df = ratings_df.pivot(index = 'userId', columns ='movieId', values = 'rating').fillna(0)
print('R_df')
print(R_df.head(10))

R = R_df.as_matrix()
print(R)
user_ratings_mean = np.mean(R, axis = 1)
R_demeaned = R - user_ratings_mean.reshape(-1, 1)

from scipy.sparse.linalg import svds
U, sigma, Vt = svds(R_demeaned, k = 2)

sigma = np.diag(sigma)

all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
preds_df = pd.DataFrame(all_user_predicted_ratings, columns = R_df.columns)

'''
   # Ref. Nick Becker, Data Scientist at Enigma Technologies
'''
def recommend_movies(predictions_df, userID, movies_df, original_ratings_df, num_recommendations=10):
    
    # Get and sort the user's predictions
    user_row_number = userID - 1 # UserID starts at 1, not 0
    sorted_user_predictions = predictions_df.iloc[user_row_number].sort_values(ascending=False)
    print(original_ratings_df)
    # Get the user's data and merge in the movie information.
    user_data = original_ratings_df[original_ratings_df.userId == str(userID)]
    user_full = (user_data.merge(movies_df, how = 'left', left_on = 'movieId', right_on = 'movieId').
                     sort_values(['rating'], ascending=False)
                 )

    print('User {0} has already rated {1} movies.'.format(userID, user_full.shape[0]))
    print('Recommending the highest {0} predicted ratings movies not already rated.'.format(num_recommendations))
    
    # Recommend the highest predicted rating movies that the user hasn't seen yet.
    recommendations = (movies_df[~movies_df['movieId'].isin(user_full['movieId'])].
         merge(pd.DataFrame(sorted_user_predictions).reset_index(), how = 'left',
               left_on = 'movieId',
               right_on = 'movieId').
         rename(columns = {user_row_number: 'Predictions'}).
         sort_values('Predictions', ascending = False).
                       iloc[:num_recommendations, :-1]
                      )

    return user_full, recommendations

already_rated, predictions = recommend_movies(preds_df, 1, movies_df, ratings_df)

print("Already Rated")
print(already_rated.head(10))

print("Predictions Recommendation")
print(predictions.head(10))
