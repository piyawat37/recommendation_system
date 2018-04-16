'''
Created on Apr 13, 2018

@author: Piyawat Pemwattana
'''

class pomServiceDto(object):

    def __init__(self, service, version, poc_version, create_date, author):
        self.service = service
        self.version = version
        self.poc_version = poc_version
        self.create_date = create_date
        self.author = author

    def get_service(self):
        return self.__service


    def get_version(self):
        return self.__version


    def get_poc_version(self):
        return self.__poc_version


    def get_create_date(self):
        return self.__create_date


    def get_author(self):
        return self.__author


    def set_service(self, value):
        self.__service = value


    def set_version(self, value):
        self.__version = value


    def set_poc_version(self, value):
        self.__poc_version = value


    def set_create_date(self, value):
        self.__create_date = value


    def set_author(self, value):
        self.__author = value


    def del_service(self):
        del self.__service


    def del_version(self):
        del self.__version


    def del_poc_version(self):
        del self.__poc_version


    def del_create_date(self):
        del self.__create_date


    def del_author(self):
        del self.__author
        
    service = property(get_service, set_service, del_service, "service's docstring")
    version = property(get_version, set_version, del_version, "version's docstring")
    poc_version = property(get_poc_version, set_poc_version, del_poc_version, "poc_version's docstring")
    create_date = property(get_create_date, set_create_date, del_create_date, "create_date's docstring")
    author = property(get_author, set_author, del_author, "author's docstring")

    def to_JSON(self):
        return {
            'service' : self.service,
            'version' : self.version,
            'poc_version' : self.poc_version,
            'create_date' : self.create_date,
            'author' : self.author
        }
