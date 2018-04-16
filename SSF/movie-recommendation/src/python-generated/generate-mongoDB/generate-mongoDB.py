'''
Created on Dec 11, 2017

@author: Piyawat Pemwattana
'''

import csv, json, os, sys, getopt, pprint, absPath

from pymongo import MongoClient

import pandas as pd


BASEDIR = absPath.csv_file_path()

mongo_client=MongoClient() 
db=mongo_client.recommendation_system


# Movies
# movies_csv_file = open(BASEDIR+'movies_test.csv', 'r', encoding="utf8")
# reader_movies = csv.DictReader(movies_csv_file)
# db.movies.drop()
# header_movies = [ "movieId", "title", "genres" ]
# try:
#     for each in reader_movies:
#         row={}
#         for field in header_movies:
#             row[field]=each[field]
#     
#         db.movies.insert(row)
#     print("Movies Success!!")
# except:
#     print("Movies UnSuccess!! Because : "+ sys.exc_info()[0])
#         
# 
# 
# # Users
# users_csv_file = open(BASEDIR+'users.csv', 'r', encoding="utf8")
# reader_users = csv.DictReader(users_csv_file)
# db.users.drop()
# header_users = [ "userId", "email", "username", "password", "status", "token", "timestamp" ]
# 
# try:
#     for each in reader_users:
#         row={}
#         for field in header_users:
#             row[field]=each[field]
#     
#         db.users.insert(row)
#     print("Users Success!!")
# except:
#     print("Users UnSuccess!! Because : ", sys.exc_info())
# 
# 
# # Ratings
# ratings_csv_file = open(BASEDIR+'ratings_test.csv', 'r', encoding="utf8")
# reader_ratings = csv.DictReader(ratings_csv_file)
# db.ratings.drop()
# header_ratings = [ "userId", "movieId", "rating", "timestamp" ]
# 
# try:
#     for each in reader_ratings:
#         row={}
#         for field in header_ratings:
#             row[field]=each[field]
#     
#         db.ratings.insert(row)
#     print("Ratings Success!!")
# except:
#     print("Ratings UnSuccess!! Because : ", sys.exc_info())
#     
#     
# # Comments
# comments_csv_file = open(BASEDIR+'comments.csv', 'r', encoding="utf8")
# reader_comments = csv.DictReader(comments_csv_file)
# db.comments.drop()
# header_comments = [ "userId", "movieId", "comment", "timestamp" ]
# 
# try:
#     for each in reader_comments:
#         row={}
#         for field in header_comments:
#             row[field]=each[field]
#     
#         db.comments.insert(row)
#     print("Comments Success!!")
# except:
#     print("Comments UnSuccess!! Because : ", sys.exc_info())
# 
# # Permissions
# permissions_csv_file = open(BASEDIR+'permissions.csv', 'r', encoding="utf8")
# reader_permissions = csv.DictReader(permissions_csv_file)
# db.permissions.drop()
# header_permissions = [ "userId", "permObj" ]
# 
# try:
#     for each in reader_permissions:
#         row={}
#         for field in header_permissions:
#             row[field]=each[field]
#     
#         db.permissions.insert(row)
#     print("Permissions Success!!")
# except:
#     print("Permissions UnSuccess!! Because : ", sys.exc_info())
    
# Train_Data
db.traindata.drop()
header_traindata = [ "userId", "movieId", "title", "genres" ]
try:
    collection = db['test-collection']
    print(collection)
    
    print("Train Data Success!!")
except:
    print("Train Data  UnSuccess!! Because : ", sys.exc_info())