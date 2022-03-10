from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from models import User

app = Flask(__name__)


app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


@app.route("/")
@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', form = form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('register.html', form = form)

@app.route("/main")
def main():
    return render_template('main.html')

