'''
Created on Dec 11, 2017

@author: Piyawat Pemwattana
'''

from random import randint

from flask import Flask, render_template, jsonify
from flask_cors.extension import CORS


app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/random')
def random_number():
    response = {
        'randomNumber': randint(1, 10)
    }
    return jsonify(response)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

app.run();