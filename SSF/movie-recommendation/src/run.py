'''
Created on Dec 11, 2017

@author: Piyawat Pemwattana
'''

from flask import Flask, render_template, jsonify, request, redirect, session, Response
from flask.helpers import url_for
from flask_cors.extension import CORS
from flask_login.login_manager import LoginManager
from flask_login.utils import login_required, logout_user 
import requests, os

import movie_service
import user_service
import common_service
import json
from userServiceDto import userServiceDto
from SystemException import SystemException
from SystemConstant import SystemConstant
from user_service import get_user_by_token, check_duplicate_user
from absPath import movies_image_path



app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
cors = CORS(app, resources={r"/common-service/*": {"origins": "*"},
                            r"/user-service/*": {"origins": "*"},
                             r"/movie-service/*": {"origins": "*"}})

app.secret_key = os.urandom(24)

exception = {}

UPLOAD_FOLDER = movies_image_path()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/common-service/')
def common_service_pom():
    pom = common_service.pom_version()
    response = {
        'msg' : '{'+pom.service+', '
                +pom.version+', '
                +pom.poc_version+', '
                +pom.create_date+', '
                +pom.author+', '
                '}'
    }
    return jsonify(response)

@app.route('/common-service/getVersion/', methods=['GET'])
def common_service_version():
    pom = common_service.pom_version()
    response = {
        'version': pom.version,
        'poc_version': pom.poc_version,
    }
    return jsonify(response)


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
        userObj = user_service.user_validate_login(movie_data=data)
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
        if check_duplicate_user(data['username'], data['email'], data['language']) == False:
            userObj = user_service.create_new_user(movie_data=data)
            response = {
                'user' : userObj.toJSON()
            }
        else:
            return check_duplicate_user(data['username'], data['email'], data['language'])
        return jsonify(response)
    
@app.route("/user-service/createAccount", methods = ['POST', 'GET'])
def create_new_account():
    if request.method == 'POST':
        data = json.loads(request.data)
        response = {}
        if check_duplicate_user(data['username'], data['email'], data['language']) == False:
            userObj = user_service.create_new_user_generate_password(movie_data=data)
            response = {
                'user' : userObj.toJSON()
            }
        else:
            return check_duplicate_user(data['username'], data['email'], data['language'])
        return jsonify(response)

@app.route('/user-service/getAllUser/', methods=['GET'])
def get_all_user():
    users = user_service.get_all_user()
    response = {
        'users' : users
    }
    print(response)
    return jsonify(response)

@app.route('/user-service/deleteAccount/<int:userId>/', methods=['DELETE'])
def delete_user(userId):
    user_service.delete_user(userId)
    response = {
    }
    return jsonify(response)

@app.route("/user-service/updateStatus", methods = ['POST', 'GET'])
def updateStatus():
    if request.method == 'POST':
        data = json.loads(request.data)
        response = {}
        userObj = user_service.update_user(userContext=data)
        response = {
            'user' : userObj.toJSON_UpdateStatus()
        }
        return jsonify(response)

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
    try:
        userObj = get_user_by_token(data)
    except:
        return Response({"Access Denined: Please, Sign in"}, status=400, mimetype='application/json')
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

@app.route('/movie-service/getMovie/', methods=['GET'])
def recommend_movie_list():
    try:
        userId = int(request.args.get("id"))
        movieList = movie_service.transform_dataFrame(userId)
    except:
        movieList = movie_service.transform_dataFrame()
        
    response = {
        'movieList': movieList
    }
    return jsonify(response)

@app.route('/movie-service/genres')
def find_list_by_genres(genres):
    
    response = {
    }
    return jsonify(response)

@app.route('/movie-service/getAllMovie/', methods=['GET'])
def get_all_movie():
    movies = movie_service.get_all_movie()
    response = {
        'movies' : movies
    }
    print(response)
    return jsonify(response)

@app.route('/movie-service/searchByString/', methods=['GET'])
def search_by_string():
    searchString = request.args.get("searchString")
    movieList = movie_service.search_by_string(searchString)
    response = {
        'movies' : movieList
    }
    print(response)
    return jsonify(response)

@app.route("/movie-service/update", methods = ['POST', 'GET'])
def update_movie():
    if request.method == 'POST':
        data = json.loads(request.data)
        response = {}
        if movie_service.check_duplicate_movie(data['title'], data['movieId'], data['language']) == False:
            movieObj = movie_service.update_movie(movieContext=data)
            response = {
                'movie' : movieObj.to_JSON_Update()
            }
        else:
            return movie_service.check_duplicate_movie(data['title'], data['movieId'], data['language'])
        return jsonify(response)
    
@app.route("/movie-service/addRating", methods = ['POST', 'GET'])
def add_rating():
    if request.method == 'POST':
        data = json.loads(request.data)
        response = {}
        ratedObj = movie_service.add_rating(ratedContext=data)
        response = {
            'userId' : ratedObj['userId']
        }
        return jsonify(response)

@app.route('/movie-service/deleteMovie/<int:movieId>/', methods=['DELETE'])
def delete_movie(movieId):
    movie_service.delete_movie(movieId)
    response = {
    }
    return jsonify(response)

@app.route("/movie-service/createMovie", methods = ['POST', 'GET'])
def create_new_movie():
    if request.method == 'POST':
        data = json.loads(request.data)
        response = {}
        if movie_service.check_duplicate_movie(title=data['title'],language=data['language']) == False:
            movieObj = movie_service.create_new_movie(movie_data=data)
            response = {
                'movie' : movieObj.to_JSON_Update()
            }
        else:
            return movie_service.check_duplicate_movie(title=data['title'], language=data['language'])
        return jsonify(response)

@app.route('/movie-service/upload', methods=['POST'])
def update_image():
    config = app.config
    file = request.files['fileImage']
    f = config.get('UPLOAD_FOLDER') + file.filename
    print(f)
    file.save(f)
    response = {
        "status" : 'File Upload Done!.'
    }
    return jsonify(response)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8082/{}'.format(path)).text
    return render_template("index.html")

if __name__ == "__main__":
    app.run(port=4996)
