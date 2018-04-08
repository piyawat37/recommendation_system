'''
Created on Dec 11, 2017

@author: Piyawat Pemwattana
'''

from flask import Flask, render_template, jsonify, request, redirect, session
from flask.helpers import url_for
from flask_cors.extension import CORS
import requests, os

import movie_service


app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"},
                            r"/common-service/*": {"origins": "*"},
                            r"/movie-service/*": {"origins": "*"}
                            })

app.secret_key = os.urandom(24)

exception = {}

@app.route('/common-service/getLang/<language>', methods=['GET'])
def set_language(language=None):
    session['language'] = language
    return redirect(url_for('index'))

''' ''' ''' ''' ''' ''' '''
    >> user-service <<
''' ''' ''' ''' ''' ''' '''
@app.route('/movie-service/')
def user_service_pom():
    pom = movie_service.pom_version()
    response = {
        'msg' : '{'+''+'}'
    }
    return render_template('render_service.html', response=response)


''' ''' ''' ''' ''' ''' '''
    >> movie-service <<
''' ''' ''' ''' ''' ''' '''
@app.route('/movie-service/')
def movie_service_pom():
    pom = movie_service.pom_version()
    response = {
        'msg' : '{'+''+'}'
    }
    return render_template('render_service.html', response=response)

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