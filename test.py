from flask import Flask, render_template, redirect, request
from requests_oauthlib import OAuth2Session
import pandas as pd
import requests

APP_ID = "01hrnv0jbne4zr0k11x45zdpcs"
API_ROOT = "https://student.sbhs.net.au/api/"
api = OAuth2Session(client_id=APP_ID, redirect_uri="https://yata.onrender.com/auth", scope="all-ro", pkce="S256")
token = ''
app = Flask(__name__)


@app.route('/')
def default():
    return redirect('/home')


@app.route('/home')
def homepage():
    return render_template('home.html')


@app.route('/main')
def main_page():
    timetable_url = API_ROOT+"timetable/daytimetable.json"
    timetable_api_response = api.get(timetable_url)
    response = timetable_api_response.json()
    timetable = [["NO DATA FOUND"]]
    if response['status'] == 'OK':
        bells = response["bells"]
        print(bells)
        timetable = response["timetable"]
        print(timetable)
    else:
        print(response)
    df = pd.DataFrame(data=timetable)
    df_html = df.to_html(border=0, index=False, header=False)
    return render_template('main.html', table_html=df_html)\


@app.route('/daily_notices')
def daily_notices():
    notices_url = API_ROOT+"dailynews/list.json"
    notices_api_response = api.get(notices_url)
    response = notices_api_response.json()
    notices = response["notices"]
    df = pd.DataFrame(data=notices)
    df_html = df.to_html(border=0, index=False, header=False)
    return render_template('daily_notices.html', daily_notices=df_html)


@app.route('/auth')
def auth():
    print(request.args)
    global token
    auth_key = request.args.get('code')
    token = api.fetch_token("https://auth.sbhs.net.au/token", authorization_code=auth_key)  # WHY THIS NO WORK >:(
    print(token)
    return redirect('/main')


@app.route('/login')
def login_page():
    global api
    url = "https://auth.sbhs.net.au/authorize"
    auth_url, state = api.authorization_url(url)
    print(state)
    print(auth_url)
    return redirect(auth_url)
# https://auth.sbhs.net.au/authorize?response_type=code&client_id=01hrnv0jbne4zr0k11x45zdpcs&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fauth&scope=all-ro&state=rnSviYURZiQGs6A2plL5ii2gg2I3Eb


if __name__ == "__main__":
    app.run()
