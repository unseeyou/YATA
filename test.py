from flask import Flask, render_template, redirect, request
from requests_oauthlib import OAuth2Session
import pandas as pd
import sqlite3

APP_ID = "01hrnv0jbne4zr0k11x45zdpcs"
API_ROOT = "https://student.sbhs.net.au/api/"
REDIRECT_URI = "https://yata.onrender.com/auth"
api = OAuth2Session(client_id=APP_ID, redirect_uri=REDIRECT_URI, scope="all-ro", pkce="S256")
token = ''
app = Flask(__name__)
conn = sqlite3.connect('static/users.db')


@app.route('/')
def default():
    return redirect('/home')


@app.route('/home')
def homepage():
    return render_template('home.html')


@app.route('/main')
def main_page():
    timetable_url = API_ROOT + "timetable/daytimetable.json"
    timetable_api_response = api.get(timetable_url)
    response = timetable_api_response.json()
    day = []
    if response['status'] == 'OK':
        bells = response["bells"]
        print(bells)
        timetable = response["timetable"]
        # print(timetable)
        subjects: dict = timetable["subjects"]
        # print(f"{subjects=}")
        periods: dict = timetable["timetable"]["periods"]
        routine = timetable["timetable"]["routine"]
        routine_items = routine.split(",")
        for item in routine_items:
            if "R" == item:
                period = {"title": "Recess", "fullTeacher": "", "room": ""}
            elif "WFL" in item:
                period = {"title": f"Lunch {item[-1]}", "fullTeacher": "", "room": ""}
            elif "RC" == item:
                period = {"title": "Roll Call", "fullTeacher": "", "room": ""}
            else:
                period = periods.get(item)
            if period is None:
                period = {"title": "", "fullTeacher": "", "room": ""}
            elif "SP" in period["title"]:
                period = {"title": "Sport", "fullTeacher": "", "room": ""}
            if period["fullTeacher"] is None:
                period["fullTeacher"] = period["teacher"]
            # print(f"{period=}")
            subject = subjects.get(period["year"]+period['title'] if period.get("year") is not None else ""+period['title'])
            # print(f"{subject=}\n{period["year"]+period['title'] if period.get("year") is not None else ""+period[
            # 'title']}")
            if subject is None:
                subject = {"title": period["title"]}
            day.append({"subject": f"{subject['title']} {period['fullTeacher']}",
                        "room": period['room']})
        day.append({"room": '', "subject": 'End of Day'})

    else:
        print(response)
    df = pd.DataFrame(data=day)
    df_html = df.to_html(border=0, index=False, header=False)
    return render_template('main.html', table_html=df_html)


@app.route('/daily_notices')
def daily_notices():
    notices_url = API_ROOT + "dailynews/list.json"
    notices_api_response = api.get(notices_url)
    response = notices_api_response.json()
    notices = response["notices"]
    df = pd.DataFrame(data=notices)
    df_html = df.to_html(border=0, index=False, header=False)
    return render_template('daily_notices.html', daily_notices=df_html)


@app.route('/auth')
def auth():
    # print(request.args)
    global token
    auth_key = request.args.get('code')
    token = api.fetch_token("https://auth.sbhs.net.au/token", code=auth_key)  # WHY THIS NO WORK >:(
    # print(token)
    return redirect('/main')


@app.route('/login')
def login_page():
    global api
    url = "https://auth.sbhs.net.au/authorize"
    auth_url, state = api.authorization_url(url)
    # print(state)
    # print(auth_url)
    return redirect(auth_url)


if __name__ == "__main__":
    app.run()
