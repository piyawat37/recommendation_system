'''
Created on Apr 28, 2018

@author: Piyawat Pemwattana
'''

class permissionServiceRepository(object):
    def __init__(self, userId, role):
        self.userId = userId
        self.role = role

    def get_user_id(self):
        return self.__userId


    def get_role(self):
        return self.__role


    def set_user_id(self, value):
        self.__userId = value


    def set_role(self, value):
        self.__role = value


    def del_user_id(self):
        del self.__userId


    def del_role(self):
        del self.__role

    def to_JSON(self):
        return {
            'userId': self.userId,
            'role': self.role
        }

    userId = property(get_user_id, set_user_id, del_user_id, "userId's docstring")
    role = property(get_role, set_role, del_role, "role's docstring")
    
    