'''
Created on Feb 10, 2018

@author: Piyawat Pemwattana
'''
from pomServiceDto import pomServiceDto
from connectMongoDB import _connect_mongo
from userServiceDto import userServiceDto
from SystemConstant import SystemConstant
import secrets

db = _connect_mongo(host='localhost', port=27017, username=None, password=None, db='recommendation_system')

def pom_version():
    pom = pomServiceDto('user-service',
                  '0.0.1-PRODUCTION',
                  '0.0.8-PROTOTYPE',
                  'Created on Feb 10, 2018',
                  'Piyawat Pemwattana')
    return pom
    
def data_test():
    return {
        'username' : 'admin',
        'password' : 'password',
        'authenticated': True
    }
    
def data_test_token():
    return {
        'token' : 'sVSUlrIhMeBbEiT7ysPTfYiXCu32-PDKWQZlw8Eu1QM',
    }

def set_hsh_password(raw_password):
        import hashlib
        preSalt = str(hashlib.sha256(SystemConstant.PRE_SALT.encode(encoding='utf_8')).hexdigest())
        postSalt = str(hashlib.sha256(SystemConstant.POST_SALT.encode(encoding='utf_8')).hexdigest())
        rawPassword = str(hashlib.sha256(raw_password.encode(encoding='utf_8')).hexdigest())
        hsh = hashlib.sha256(preSalt.encode(encoding='utf_8')
                             +postSalt.encode(encoding='utf_8')
                             +rawPassword.encode(encoding='utf_8')).hexdigest()
        return hsh

def user_validate_login(user_data):
    user = db['users'].find_one({'username' : user_data['username']})
    is_authenticated = False
    #check
    if user != None:
        current_password = user['password']
        criteria_password = set_hsh_password(raw_password=user_data['password']) 
        #authen
        if current_password == criteria_password:
            is_authenticated = True
            db['users'].find_one_and_update({'userId':user['userId']}, {'$set': {'token': secrets.token_urlsafe()}})
            user = db['users'].find_one({'username' : user_data['username']})
            userObj = userServiceDto(userId=user['userId']
                                 , email=user['email']
                                 , username=user['username']
                                 , status=user['status']
                                 , is_authenticated=is_authenticated
                                 , token=user['token'])
        return userObj
    else:
        userObj = userServiceDto(userId=None,
                                  email=None,
                                   username=user_data['username'],
                                    status=None,
                                     is_authenticated=is_authenticated,
                                      token=None)
        return userObj
        
def get_user_by_token(access):
    user = db['users'].find_one({'token' : access['token']})
    is_authenticated = False
    if user != None:
        is_authenticated = True
        userObj = userServiceDto(userId=user['userId']
                 , email=user['email']
                 , username=user['username']
                 , status=user['status']
                 , is_authenticated=is_authenticated
                 , token=user['token'])
        return userObj
    
    
# userObj = get_user_by_token(access=data_test_token())

# print(userObj.get_username())
#    
# print(userObj.get_user_id())
# print(userObj.get_email())
# print(userObj.get_username())
# print(userObj.get_status())
# print(userObj.get_is_authenticated())
# print(userObj.get_token())
