'''
Created on Dec 11, 2017

@author: Piyawat Pemwattana
'''

from random import randint
from flask import Flask, render_template, jsonify
from flask_cors.extension import CORS
from pymongo import MongoClient # Database connector
import pandas
import numpy

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

client = MongoClient('localhost', 27017)
db = client.recommendation_system

def get_all_object():
    movie_obj = db.movies.find()
    rating_obj = db.ratings.find()
    return movie_obj, rating_obj

movie_obj, rating_obj = get_all_object()

rating_obj = db.ratings.find({'userId': '1'})
ratingsDataFrame = pandas.DataFrame(list(rating_obj), columns = ['userId', 'movieId', 'rating', 'timestamp'], dtype = int);
ratingsDataFrame['userId'] = ratingsDataFrame['userId'].astype(int)
ratingsDataFrame['movieId'] = ratingsDataFrame['movieId'].astype(int)
# ratingsDataFrame['rating'] = ratingsDataFrame['rating'].astype(float)
# ratingsDataFrame['rating'] = ratingsDataFrame['rating'].astype(int)
ratingsDataFrame['rating'] = ratingsDataFrame['rating'].astype(numpy.float64)


moviesDataFrame = pandas.DataFrame(list(movie_obj));
moviesDataFrame['movieId'] = moviesDataFrame['movieId'].apply(pandas.to_numeric)

print(ratingsDataFrame.head())

joinDataFrame = ratingsDataFrame.pivot(index='userId', columns='movieId', values='rating').fillna(0)
joinMatrix = joinDataFrame.as_matrix()
 
# print(moviesDataFrame.head(10))
print(joinMatrix.shape)

@app.route('/api/random')
def random_number(): 
    response = {
        'randomNumber': randint(1,10)
    }
    return jsonify(response)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


result = []

# def matrix_factorization(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
#     Q = Q.T
#     print("QT")
#     print(Q)
#     for step in range(steps):
#         for i in range(len(R)):
#             for j in range(len(R[i])):
#                 if R[i][j] > 0:
#                     eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])
#                     for k in range(K):
#                         P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
#                         Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
#         eR = numpy.dot(P,Q)
#         ## List Learning input when every 500
#         if(step%500 == 0):
#             result.append(eR)
#         # print(eR)
#         e = 0
#         for i in range(len(R)):
#             for j in range(len(R[i])):
#                 if R[i][j] > 0:
#                     e = e + pow(R[i][j] - numpy.dot(P[i,:],Q[:,j]), 2)
#                     for k in range(K):
#                         e = e + (beta/2) * ( pow(P[i][k],2) + pow(Q[k][j],2) )
#         if e < 0.001:
#             break
#     return P, Q.T

###############################################################################

# if __name__ == "__main__":
# 
#     R = numpy.array(ratingsDataFrame)
# 
#     N = len(R)
#     M = len(R[0])
#     K = 2
# 
#     P = numpy.random.rand(N,K)
#     Q = numpy.random.rand(M,K)
#     # print("Q")
#     # print(Q)
#     nP, nQ = matrix_factorization(R, P, Q, K)
#     for index, temp in enumerate(result):
#         print('Iteration :'+ str(index*500))
#         print(temp)
#     nR = numpy.dot(nP, nQ.T)
#     print("np : ")
#     print(nP)
#     print("nQ : ")
#     print(nQ)
#     print("nR : ")
#     print(nR)

    
app.run();