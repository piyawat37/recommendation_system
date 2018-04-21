'''
Created on Apr 1, 2018

@author: Piyawat Pemwattana
'''

class userServiceRepository(object):

    def __init__(self, userId, email, username, password, status, token, timestamp):
        self.userId = userId
        self.email = email
        self.username = username
        self.password = password
        self.status = status
        self.token = token
        self.timestamp = timestamp

    def get_user_id(self):
        return self.__userId


    def get_email(self):
        return self.__email


    def get_username(self):
        return self.__username


    def get_password(self):
        return self.__password


    def get_status(self):
        return self.__status


    def get_token(self):
        return self.__token


    def get_timestamp(self):
        return self.__timestamp


    def set_user_id(self, value):
        self.__userId = value


    def set_email(self, value):
        self.__email = value


    def set_username(self, value):
        self.__username = value


    def set_password(self, value):
        self.__password = value


    def set_status(self, value):
        self.__status = value


    def set_token(self, value):
        self.__token = value


    def set_timestamp(self, value):
        self.__timestamp = value


    def del_user_id(self):
        del self.__userId


    def del_email(self):
        del self.__email


    def del_username(self):
        del self.__username


    def del_password(self):
        del self.__password


    def del_status(self):
        del self.__status


    def del_token(self):
        del self.__token


    def del_timestamp(self):
        del self.__timestamp

    def to_JSON(self):
        return {
            'userId' : self.get_user_id(),
            'email' : self.get_email(),
            'username' : self.get_username(),
            'password' : self.get_password(),
            'status' : self.get_status(),
            'token' : self.get_token(),
            'timestamp' : self.get_timestamp()
        }

    userId = property(get_user_id, set_user_id, del_user_id, "userId's docstring")
    email = property(get_email, set_email, del_email, "email's docstring")
    username = property(get_username, set_username, del_username, "username's docstring")
    password = property(get_password, set_password, del_password, "password's docstring")
    status = property(get_status, set_status, del_status, "status's docstring")
    token = property(get_token, set_token, del_token, "token's docstring")
    timestamp = property(get_timestamp, set_timestamp, del_timestamp, "timestamp's docstring")

    