'''
Created on Dec 11, 2017

@author: Piyawat Pemwattana
'''
# import absPath, csv
# import numpy as np
# from scipy.sparse import csr_matrix
# from sparsesvd import sparsesvd
# 
# CSVFILE_DIR = absPath.csv_file_path()
# 
# MAX_UID = 800
# MAX_PID = 190000
# 
# def readUrm():
#     urm = np.zeros(shape=(MAX_UID,MAX_PID), dtype=np.float32)
#     with open(CSVFILE_DIR + 'ratings.csv', 'rt') as trainFile:
#         urmReader = csv.reader(trainFile, delimiter=',')
#         next(urmReader, None)
#         for row in urmReader:
#             urm[int(row[0]), int(row[1])] = float(row[2]) 
#     return csr_matrix(urm, dtype=np.float32)
#     
# def getMoviesSeen():
#     moviesSeen = dict()
#     with open(CSVFILE_DIR + "movies_test.csv", 'rt') as trainFile:
#         urmReader = csv.reader(trainFile, delimiter=',')
#         next(urmReader, None)
#         for row in urmReader:
#             try:
#                 moviesSeen[int(row[0])] = list()
#             except:
#                 moviesSeen[row[0]] = list()
# #         for row in moviesSeen:
# #             print(row)
#     return moviesSeen
#         
# def readUsersTest():
#     uTest = dict()
#     with open(CSVFILE_DIR + "users.csv", 'rt') as testFile:
#         testReader = csv.reader(testFile, delimiter=',')
#         next(testReader, None)
#         for row in testReader:
#             try:
#                 uTest[int(row[0])] = list()
#             except:
#                 uTest[(row[0])] = list()
# #         print(uTest)
# #         for row in uTest:
# #             print(row)
#     return uTest
# 
# def computeSVD(urm, K):
#     U, s, Vt = sparsesvd(urm, K)
# 
#     dim = (len(s), len(s))
#     S = np.zeros(dim, dtype=np.float32)
#     for i in range(0, len(s)):
#         S[i,i] = mt.sqrt(s[i])
# 
#     U = csr_matrix(np.transpose(U), dtype=np.float32)
#     S = csr_matrix(S, dtype=np.float32)
#     Vt = csr_matrix(Vt, dtype=np.float32)
# 
#     return U, S, Vt    
# 
# 
# from scipy.sparse.linalg import *  # used for matrix multiplication
# 
# 
# def computeEstimatedRatings(urm, U, S, Vt, uTest, moviesSeen, K, test):
#     rightTerm = S*Vt 
# 
#     estimatedRatings = np.zeros(shape=(MAX_UID, MAX_PID), dtype=np.float16)
#     for userTest in uTest:
#         prod = U[userTest, :]*rightTerm
# 
#         #we convert the vector to dense format in order to get the indices of the movies with the best estimated ratings 
#         estimatedRatings[userTest, :] = prod.todense()
#         recom = (-estimatedRatings[userTest, :]).argsort()[:250]
#         for r in recom:
#             if r not in moviesSeen[userTest]:
#                 uTest[userTest].append(r)
# 
#                 if len(uTest[userTest]) == 5:
#                     break
# 
#     return uTest
# 
# def main():
#     K = 90
#     urm = readUrm()
#     U, S, Vt = computeSVD(urm, K)
#     uTest = readUsersTest()
#     moviesSeen = getMoviesSeen()
#     uTest = computeEstimatedRatings(urm, U, S, Vt, uTest, moviesSeen, K, True)
#     
# main()