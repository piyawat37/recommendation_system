'''
Created on Dec 11, 2017

@author: Piyawat Pemwattana
'''

import pandas as pd
import numpy as np
import absPath

ratings_list = [i.strip().split(",") for i in open(absPath.csv_file_path() + '/ratings_test.csv', 'r').readlines()]
users_list = [i.strip().split(",") for i in open(absPath.csv_file_path() + '/users.csv', 'r').readlines()]
movies_list = [i.strip().split(",") for i in open(absPath.csv_file_path() + '/movies.csv', 'r', encoding='utf8').readlines()]

ratings_df = pd.DataFrame(ratings_list, columns = ['UserID', 'MovieID', 'Rating', 'Timestamp'], dtype = int)
ratings_df.loc[0] = [1, 5377, 4, 1206759144]  # adding a row
ratings_df.index = ratings_df.index + 1  # shifting index
ratings_df = ratings_df.sort_index()  # sorting by index
print(ratings_df)
print("----------------------------------------------------")
print(ratings_df.dtypes)
for index, val in enumerate(movies_list):
    if len(val) > 3:
        movies_list[index] = [val[0], ','.join(val[1:len(val) - 1]), val[-1]]
movies_df = pd.DataFrame(movies_list, columns = ['MovieID', 'Title', 'Genres'])
movies_df.drop(movies_df.index[:1], inplace=True)
movies_df['MovieID'] = movies_df['MovieID'].apply(pd.to_numeric)
ratings_df['Rating'] = ratings_df['Rating'].apply(pd.to_numeric)
   

print(movies_df.head())
print(ratings_df.head())
R_df = ratings_df.pivot(index = 'UserID', columns ='MovieID', values = 'Rating').fillna(0)
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
    Ref. Nick Becker, Data Scientist at Enigma Technologies
'''
def recommend_movies(predictions_df, userID, movies_df, original_ratings_df, num_recommendations=10):
    
    # Get and sort the user's predictions
    user_row_number = userID - 1 # UserID starts at 1, not 0
    sorted_user_predictions = predictions_df.iloc[user_row_number].sort_values(ascending=False)
    
    # Get the user's data and merge in the movie information.
    user_data = original_ratings_df[original_ratings_df.UserID == (userID)]
    user_full = (user_data.merge(movies_df, how = 'left', left_on = 'MovieID', right_on = 'MovieID').
                     sort_values(['Rating'], ascending=False)
                 )

    print('User {0} has already rated {1} movies.'.format(userID, user_full.shape[0]))
    print('Recommending the highest {0} predicted ratings movies not already rated.'.format(num_recommendations))
    
    # Recommend the highest predicted rating movies that the user hasn't seen yet.
    recommendations = (movies_df[~movies_df['MovieID'].isin(user_full['MovieID'])].
         merge(pd.DataFrame(sorted_user_predictions).reset_index(), how = 'left',
               left_on = 'MovieID',
               right_on = 'MovieID').
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
