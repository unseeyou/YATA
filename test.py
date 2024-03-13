from flask import Flask, render_template, redirect, request
from werkzeug.datastructures import MultiDict

app = Flask(__name__)


@app.route('/')
def default():
    return redirect('/home')


@app.route('/home')
def homepage():
    return render_template('home.html')


@app.route('/auth')
def auth_page():
    querystring = request.args
    print(querystring.get('authToken', default=None, type=str))
    return redirect('/home')


if __name__ == "__main__":
    app.run()
