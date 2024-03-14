from flask import Flask, render_template, redirect, request
from requests_oauthlib import OAuth2Session
import pandas as pd
import requests

APP_ID = "01hrnv0jbne4zr0k11x45zdpcs"
app = Flask(__name__)


@app.route('/')
def default():
    return redirect('/home')


@app.route('/home')
def homepage():
    return render_template('home.html')


@app.route('/main')
def main_page():
    df = pd.DataFrame(data=[[1,2],[3,4]])
    df_html = df.to_html(border=0, header=False, index=False)
    return render_template('main.html', table_html=df_html)


@app.route('/auth')
def auth():
    print(request.args)
    global auth_key
    auth_key = request.args.get('code')
    return redirect('/main')


@app.route('/login')
def login_page():
    url = "https://auth.sbhs.net.au/authorize"
    api = OAuth2Session(client_id=APP_ID, redirect_uri="https://yata.onrender.com/auth", scope="all-ro", pkce="S256")
    auth_url, state = api.authorization_url(url)
    print(state)
    print(auth_url)
    return redirect(auth_url)
# https://auth.sbhs.net.au/authorize?response_type=code&client_id=01hrnv0jbne4zr0k11x45zdpcs&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fauth&scope=all-ro&state=rnSviYURZiQGs6A2plL5ii2gg2I3Eb


if __name__ == "__main__":
    app.run()
