from flask import Flask, render_template, redirect, request
from requests_oauthlib import OAuth2Session
import requests

APP_ID = "01hrnv0jbne4zr0k11x45zdpcs"
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
    print(querystring.get('code', default=None, type=str))
    return redirect('/home')


@app.route('/login')
def login_page():
    url = "https://auth.sbhs.net.au/authorize"
    api = OAuth2Session(client_id=APP_ID, redirect_uri="https://yata.onrender.com/auth", scope="all-ro", pkce="plain", )
    auth_url, state = api.authorization_url(url)
    print(state)
    print(auth_url)
    # token = api.fetch_token(token_url="https://auth.sbhs.net.au/token")
    return str(auth_url)
# https://auth.sbhs.net.au/authorize?response_type=code&client_id=01hrnv0jbne4zr0k11x45zdpcs&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fauth&scope=all-ro&state=rnSviYURZiQGs6A2plL5ii2gg2I3Eb


if __name__ == "__main__":
    app.run()
