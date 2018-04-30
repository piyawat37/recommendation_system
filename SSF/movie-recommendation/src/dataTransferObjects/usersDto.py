'''
Created on Apr 30, 2018

@author: Piyawat Pemwattana
'''

class usersDto(object):
    

    def __init__(self, userId=None, email=None, username=None, status=None):
        self.userId = userId
        self.email = email
        self.username = username
        self.status = status

    def get_user_id(self):
        return self.__userId


    def get_email(self):
        return self.__email


    def get_username(self):
        return self.__username


    def get_status(self):
        return self.__status


    def set_user_id(self, value):
        self.__userId = value


    def set_email(self, value):
        self.__email = value


    def set_username(self, value):
        self.__username = value


    def set_status(self, value):
        self.__status = value


    def del_user_id(self):
        del self.__userId


    def del_email(self):
        del self.__email


    def del_username(self):
        del self.__username


    def del_status(self):
        del self.__status

    userId = property(get_user_id, set_user_id, del_user_id, "userId's docstring")
    email = property(get_email, set_email, del_email, "email's docstring")
    username = property(get_username, set_username, del_username, "username's docstring")
    status = property(get_status, set_status, del_status, "status's docstring")
    
    def to_JSON(self):
        return {
            'userId' : self.userId,
            'username' : self.username,
            'email' : self.email,
            'status' : self.status
        }
        
    
    