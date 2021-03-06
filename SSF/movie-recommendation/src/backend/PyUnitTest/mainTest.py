'''
Created on Jan 1, 2018

@author: Piyawat Pemwattana
'''
import unittest, csv, absPath
import numpy as np
from scipy.sparse import csr_matrix

CSVFILE_DIR = absPath.csv_file_path()

MAX_UID = 671
MAX_PID = 9066

class Test(unittest.TestCase):

    def test_readUrm(self):
        urm = np.zeros(shape=(MAX_UID,MAX_PID), dtype=np.float32)
        with open(CSVFILE_DIR + 'ratings.csv', 'rt') as trainFile:
            urmReader = csv.reader(trainFile, delimiter=',')
            next(urmReader, None)
            for row in urmReader:
                urm[int(row[0]), int(row[1])] = float(row[2])
                    
            print (csr_matrix(urm, dtype=np.float32))
        
    def test_getMoviesSeen(self):
        moviesSeen = dict()
        with open(CSVFILE_DIR + "movies_test.csv", 'rt') as trainFile:
            urmReader = csv.reader(trainFile, delimiter=',')
            next(urmReader, None)
            for row in urmReader:
                try:
                    moviesSeen[int(row[0])] = list()
                except:
                    moviesSeen[row[0]] = list()
#         for row in moviesSeen:
#             print(row)
        print(moviesSeen)
            
    def test_readUsersTest(self):
        uTest = dict()
        with open(CSVFILE_DIR + "users.csv", 'rt') as testFile:
            testReader = csv.reader(testFile, delimiter=',')
            next(testReader, None)
            for row in testReader:
                try:
                    uTest[int(row[0])] = list()
                except:
                    uTest[(row[0])] = list()
#         print(uTest)
#         for row in uTest:
#             print(row)
        print(uTest)

if __name__ == "__main__":
#     import sys;sys.argv = ['', 'Test.readUsersTest']
    unittest.main()