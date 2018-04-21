'''
Created on Dec 11, 2017

@author: Piyawat Pemwattana
'''

from flask import Flask, render_template, jsonify, request, redirect, session, Response
import flask
from flask.helpers import url_for
from flask_cors.decorator import cross_origin
from flask_cors.extension import CORS
from flask_login.login_manager import LoginManager
from flask_login.utils import login_required, login_user, logout_user 
import requests, os

import movie_service
from userServiceDto import userServiceDto
import user_service
import json
from SystemException import SystemException
from SystemConstant import SystemConstant
from user_service import get_user_by_token, check_duplicate_user



app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
cors = CORS(app, resources={r"/common-service/*": {"origins": "*"},
                            r"/user-service/*": {"origins": "*"},
                             r"/movie-service/*": {"origins": "*"}})

app.secret_key = os.urandom(24)

exception = {}

@app.route('/user-service/getpost', methods = ['POST', 'GET'])
def postGetHandler():
    if request.method == 'POST':
        return 'request via POST'
    else:
        return 'request via GET'

@app.route('/common-service/getLang/<language>', methods=['GET'])
def set_language(language=None):
    session['language'] = language
    return redirect(url_for('index'))

''' ''' ''' ''' ''' ''' '''
    >> user-service <<
''' ''' ''' ''' ''' ''' '''
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/user-service/')
def user_service_pom():
    pom = user_service.pom_version()
    response = {
        'msg' : '{'+pom.service+', '
                +pom.version+', '
                +pom.poc_version+', '
                +pom.create_date+', '
                +pom.author+', '
                '}'
    }
    return jsonify(response)
# somewhere to login

@app.route("/user-service/signIn", methods = ['POST', 'GET'])
def signIn():
    if request.method == 'POST':
        data = json.loads(request.data)
        response = {}
        userObj = user_service.user_validate_login(user_data=data)
        if userObj.get_is_authenticated() == True:
            if userObj.get_status == SystemConstant.STATUS_I: 
                try:
                    raise SystemException(SystemException.message_validate_signIn_status(None, data['language']))
                except SystemException as error:
                    print(error)
                    resp = Response({SystemException.message_validate_signIn_status(None, data['language'])}, status=400, mimetype='application/json')
                    return resp
                    
            else:
                response ={
                    'user' : userObj.toJSON()
                }
                return jsonify(response)
        else:
            try:
                raise SystemException(SystemException.message_validate_not_authen(None, data['language']))
            except SystemException as error:
                print(error)
                resp = Response({SystemException.message_validate_not_authen(None, data['language'])}, status=400, mimetype='application/json')
                return resp

@app.route("/user-service/signUp", methods = ['POST', 'GET'])
def signUp():
    if request.method == 'POST':
        data = json.loads(request.data)
        response = {}
        print(data['email'])
        print(data['username'])
        print(data['password'])
        print(data['language'])
        if check_duplicate_user(data['username'], data['email'], data['language']) == False:
            userObj = user_service.create_new_user(user_data=data)
            response = {
                'user' : userObj.toJSON()
            }
        else:
            return check_duplicate_user(data['username'], data['email'], data['language'])
        return response

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')

@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')

@login_manager.user_loader
def load_user(userId):
    return userServiceDto(userId)

@app.route("/user-service/authenByToken", methods = ['POST', 'GET'])
def getUserByToken():
    data = json.loads(request.data)
    userObj = get_user_by_token(data)
    response ={
        'user' : userObj.toJSON()
    }
    return jsonify(response)
        

''' ''' ''' ''' ''' ''' '''
    >> movie-service <<
''' ''' ''' ''' ''' ''' '''
@app.route('/movie-service/')
def movie_service_pom():
    pom = movie_service.pom_version()
    response = {
        'msg' : '{'+pom.service+', '
                +pom.version+', '
                +pom.poc_version+', '
                +pom.create_date+', '
                +pom.author+', '
                '}'
    }
    return jsonify(response)

@app.route('/movie-service/getMovieByUserId/', methods=['GET'])
def recommend_movie_list():
    userId = int(request.args.get("id"))
    lang = request.args.get("language")
    session['lang'] = lang
    movieList = movie_service.transform_dataFrame(userId)
    response = {
        'movieList': movieList
    }
    return jsonify(response)

@app.route('/movie-service/genres')
def find_list_by_genres(genres):
    
    response = {
    }
    return jsonify(response)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")



app.run();