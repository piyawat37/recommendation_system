'''
Created on Apr 1, 2018

@author: Piyawat Pemwattana
'''

class userServiceDto(object):

    def __init__(self, userId, email, username, status, is_authenticated, token):
        self.userId = userId
        self.email = email
        self.username = username
        self.status = status
        self.is_authenticated = is_authenticated
        self.token = token

    def get_user_id(self):
        return self.__userId


    def get_email(self):
        return self.__email


    def get_username(self):
        return self.__username


    def get_status(self):
        return self.__status


    def get_is_authenticated(self):
        return self.__is_authenticated


    def get_token(self):
        return self.__token


    def set_user_id(self, value):
        self.__userId = value


    def set_email(self, value):
        self.__email = value


    def set_username(self, value):
        self.__username = value


    def set_status(self, value):
        self.__status = value


    def set_is_authenticated(self, value):
        self.__is_authenticated = value


    def set_token(self, value):
        self.__token = value


    def del_user_id(self):
        del self.__userId


    def del_email(self):
        del self.__email


    def del_username(self):
        del self.__username


    def del_status(self):
        del self.__status


    def del_is_authenticated(self):
        del self.__is_authenticated


    def del_token(self):
        del self.__token

    def toJSON(self):
        return {
            'userId': self.userId,
            'email': self.email,
            'username': self.username,
            'status': self.status,
            'is_authenticated': self.is_authenticated,
            'token': self.token
        }

    userId = property(get_user_id, set_user_id, del_user_id, "userId's docstring")
    email = property(get_email, set_email, del_email, "email's docstring")
    username = property(get_username, set_username, del_username, "username's docstring")
    status = property(get_status, set_status, del_status, "status's docstring")
    is_authenticated = property(get_is_authenticated, set_is_authenticated, del_is_authenticated, "is_authenticated's docstring")
    token = property(get_token, set_token, del_token, "token's docstring")
        
