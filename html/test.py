# first to run in terminal: FLASK_APP=test.py flask run
# Tutorial: http://flask.pocoo.org/docs/0.12/quickstart/#a-minimal-application
# http://localhost:5000/hello/Lucas%20hahaha%20hahaha will work for this code
# from flask import Flask, request
# app = Flask(__name__)
#
# @app.route("/")
# def hello():
#     return "Hello World!"
#
# @app.route("/hello/<name>")
# def helloa(name):
#     return "GA WEG %s" % name
#
# @app.route('/query', methods=['POST', 'GET'])
# def queryhandler():
#     if request.method == 'POST':
#         query_input = request.form['questionbar']
#         return query_input
#     elif request.method == 'GET':
#         return 'GET'
#     else:
#         return "ERROR"

from flask import Flask, jsonify, render_template, request
app = Flask(__name__)

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/')
def index():
    return render_template('test.html')
