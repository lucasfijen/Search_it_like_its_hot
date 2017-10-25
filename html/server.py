# first to run in terminal: FLASK_APP=test.py flask run
# Tutorial: http://flask.pocoo.org/docs/0.12/quickstart/#a-minimal-application
# http://localhost:5000/hello/Lucas%20hahaha%20hahaha will work for this code
#
# https://codehandbook.org/python-flask-jquery-ajax-post/
from flask import Flask, request, jsonify
from flask import render_template
import queryhandler as handle

app = Flask(__name__)

@app.route("/hello/<name>")
def helloa(name):
    return "GA WEG %s" % name


@app.route('/tryout', methods=['POST'])
def handlerhandler():
    if request.method == 'POST':
        text = request.form.get('questionbar')
        # return text
        result = handle.query_handler(text)
        return result
    else:
        return 'ELSE'


@app.route('/')
def testpage():
    return render_template('test.html')

if __name__ == "__main__":
    app.run()
