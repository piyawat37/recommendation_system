'''
Created on Dec 11, 2017

@author: Piyawat Pemwattana
'''

from random import randint
from flask import Flask, render_template, jsonify, request, redirect
from flask_cors.extension import CORS
from pymongo import MongoClient # Database connector
from nt import abort
from flask.helpers import url_for
from ctypes.test.test_pickling import name

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

exception = {}

@app.route('/api/random', methods=['POST'])
def random_number(): 
    response = {
        'randomNumber': randint(1,10)
    }
    return jsonify(response)


@app.route('/success/<user>')
def success(user):
    return 'Success %s' %user

@app.route('/signin', methods=['POST','GET'])
def sign_in():
    if request.method == 'POST':
        userId = request.form['userId']
        return redirect(url_for('Success', user = userId))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

result = []

app.run();