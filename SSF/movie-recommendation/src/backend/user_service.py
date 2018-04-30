'''
Created on Feb 10, 2018

@author: Piyawat Pemwattana
'''
import secrets
import time

from flask import Response
import pymongo

from SystemConstant import SystemConstant
from SystemException import SystemException
from SystemMessage import SystemMessage
from connectMongoDB import _connect_mongo
from pomServiceDto import pomServiceDto
from userServiceDto import userServiceDto
from userServiceRepository import userServiceRepository
from permissionsServiceRepository import permissionServiceRepository
from usersDto import usersDto


db = _connect_mongo(host='localhost', port=27017, username=None, password=None, db='recommendation_system')

def pom_version():
    pom = pomServiceDto('user-service',
                  '1.0.0',
                  '0.0.10-PROTOTYPE',
                  'Created on Feb 10, 2018',
                  'Piyawat Pemwattana')
    return pom
    
def data_test():
    return {
        'email' : 'email1@email.com',
        'username' : 'adminnn1',
        'password' : 'password',
        'language' : 'EN'
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
            user_map_role = db['permissions'].find_one({'userId' : user['userId']})
            userObj = userServiceDto(userId=user['userId']
                                 , email=user['email']
                                 , username=user['username']
                                 , status=user['status']
                                 , is_authenticated=is_authenticated
                                 , token=user['token']
                                 , role=user_map_role['role'])
        return userObj
    else:
        userObj = userServiceDto(userId=None,
                                  email=None,
                                   username=user_data['username'],
                                    status=None,
                                     is_authenticated=is_authenticated,
                                      token=None,
                                        role=None)
        return userObj
        
def get_user_by_token(access):
    user = db['users'].find_one({'token' : access['token']})
    user_map_role = db['permissions'].find_one({'userId' : user['userId']})
    is_authenticated = False
    if user != None:
        is_authenticated = True
        userObj = userServiceDto(userId=user['userId']
                 , email=user['email']
                 , username=user['username']
                 , status=user['status']
                 , is_authenticated=is_authenticated
                 , token=user['token']
                 , role=user_map_role['role'])
        return userObj
    
def check_duplicate_user(username, email, language):
    isDuplicate = False
    
    if db['users'].find_one({'email' : email}) != None:
        try:
            raise SystemException(SystemException.message_duplicate_context(None, SystemMessage.Msg['emailException-'+language], language))
        except SystemException as error:
            resp = Response({SystemException.message_duplicate_context(None, SystemMessage.Msg['emailException-'+language], language)}, status=400, mimetype='application/json')
            return resp
        
    if db['users'].find_one({'username' : username}) != None:
        try:
            raise SystemException(SystemException.message_duplicate_context(None, SystemMessage.Msg['usernameException-'+language], language))
        except SystemException as error:
            resp = Response({SystemException.message_duplicate_context(None, SystemMessage.Msg['usernameException-'+language], language)}, status=400, mimetype='application/json')
            return resp
    
    
    return isDuplicate

def create_new_user(user_data):
    if check_duplicate_user(user_data['username'], user_data['email'], user_data['language']) == False:
        userGetMax = db.users.find().sort('userId', -1).limit(1)
        userId = ''
        for cursor in userGetMax:
            userId = int(cursor['userId'])+1
        userRepoObj = userServiceRepository(userId=userId
                     , email=user_data['email']
                     , username=user_data['username']
                     , password=set_hsh_password(user_data['password'])
                     , status=SystemConstant.STATUS_A
                     , token=secrets.token_urlsafe()
                     , timestamp="%d " %  time.time())
        db.users.insert_one(userRepoObj.to_JSON())
        userObj = db['users'].find_one({'userId' : userId})
        permissionRepoObj = permissionServiceRepository(userId=userObj['userId']
                                                        , role=SystemConstant.ROLE_USER)
        db.permissions.insert_one(permissionRepoObj.to_JSON())
        user_role = db['permissions'].find_one({'userId': userId})
        userServiceObj = userServiceDto(userId=userObj['userId'],email=userObj['email'],username=userObj['username'],status=userObj['status'], is_authenticated=True,token=userObj['token'], role=user_role['role'])
        return userServiceObj
    else:
        return check_duplicate_user(user_data['username'], user_data['email'], user_data['language'])

def create_new_user_generate_password(user_data):
    if check_duplicate_user(user_data['username'], user_data['email'], user_data['language']) == False:
        userGetMax = db.users.find().sort('userId', -1).limit(1)
        userId = ''
        for cursor in userGetMax:
            userId = int(cursor['userId'])+1
        userRepoObj = userServiceRepository(userId=userId
                     , email=user_data['email']
                     , username=user_data['username']
                     , password=set_hsh_password('password')
                     , status=SystemConstant.STATUS_A
                     , token=secrets.token_urlsafe()
                     , timestamp="%d " %  time.time())
        db.users.insert_one(userRepoObj.to_JSON())
        userObj = db['users'].find_one({'userId' : userId})
        permissionRepoObj = permissionServiceRepository(userId=userObj['userId']
                                                        , role=SystemConstant.ROLE_USER)
        db.permissions.insert_one(permissionRepoObj.to_JSON())
        user_role = db['permissions'].find_one({'userId': userId})
        userServiceObj = userServiceDto(userId=userObj['userId'],email=userObj['email'],username=userObj['username'],status=userObj['status'], is_authenticated=True,token=userObj['token'], role=user_role['role'])
        return userServiceObj
    else:
        return check_duplicate_user(user_data['username'], user_data['email'], user_data['language'])

def get_all_user():
    users = db['users']
    usersList = []
    cursor = users.find({})
    for value in cursor:
        userDto = usersDto(value['userId'], value['email'], value['username'], value['status'])
        usersList.append(userDto.to_JSON())
    return usersList

def update_user(userContext):
    db['users'].find_one_and_update({'userId':userContext['userId']}, {'$set': {'status': userContext['status']}})
    user = db['users'].find_one({'username' : userContext['username']})
    userObjDto = userServiceDto(userId=user['userId']
                                , email=user['email']
                                , username=user['username']
                                , status=user['status']
                                , is_authenticated=None
                                , token=None
                                , role=None)
    return userObjDto

def delete_user(userId):
    db.users.delete_one({'userId':userId})

# create_new_user(data_test())
# delete_user(7)
