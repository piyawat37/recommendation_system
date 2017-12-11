'''
Created on Dec 11, 2017

@author: Piyawat Pemwattana
'''

import csv
import json
import os
import pandas as pd
import sys, getopt, pprint
from pymongo import MongoClient

BASEDIR = os.path.dirname(os.path.realpath(__file__)) + '\\csv-file\\'

mongo_client=MongoClient() 
db=mongo_client.recommendation_system


# Movies
movies_csv_file = open(BASEDIR+'movies.csv', 'r', encoding="utf8")
reader_movies = csv.DictReader(movies_csv_file)
db.movies.drop()
header_movies = [ "movieId", "title", "genres"]
try:
    for each in reader_movies:
        row={}
        for field in header_movies:
            row[field]=each[field]
    
        db.movies.insert(row)
    print("Movies Success!!")
except:
    print("Movies UnSuccess!! Because : "+ sys.exc_info()[0])
        


# Users
users_csv_file = open(BASEDIR+'users.csv', 'r', encoding="utf8")
reader_users = csv.DictReader(users_csv_file)
db.users.drop()
header_users = [ "userId", "username", "password", "timestamp"]

try:
    for each in reader_users:
        row={}
        for field in header_users:
            row[field]=each[field]
    
        db.users.insert(row)
    print("Users Success!!")
except:
    print("Users UnSuccess!! Because : ", sys.exc_info())


# Ratings
ratings_csv_file = open(BASEDIR+'ratings.csv', 'r', encoding="utf8")
reader_ratings = csv.DictReader(ratings_csv_file)
db.ratings.drop()
header_ratings = [ "userId", "movieId", "rating", "timestamp"]

try:
    for each in reader_ratings:
        row={}
        for field in header_ratings:
            row[field]=each[field]
    
        db.ratings.insert(row)
    print("Ratings Success!!")
except:
    print("Ratings UnSuccess!! Because : ", sys.exc_info())