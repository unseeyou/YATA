from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route('/')
def default():
    return redirect('/home')


@app.route('/home')
def homepage():
    return render_template('home.html')


if __name__ == "__main__":
    app.run()
