'''
Created on Apr 1, 2018

@author: Piyawat Pemwattana
'''

class userServiceRepository(object):

    def __init__(self, userId, email, username, status, token, timestamp):
        self.userId = userId
        self.email = email
        self.username = username
        self.status = status
        self.token = token
        self.timestamp = timestamp


