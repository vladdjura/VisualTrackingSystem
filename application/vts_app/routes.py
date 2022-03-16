from flask import render_template, url_for, redirect, request
from vts_app.forms import RegistrationForm, LoginForm, ParkingSpaceForm
from vts_app.styles import input_error, input_ok, submit, input_main
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
from vts_app.models import User
from vts_app import app, db, bcrypt


@app.route("/")
@app.route("/login")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('api'))
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main'))
    return render_template('login.html', 
                            form = form,
                            input_error = input_error,
                            input_ok = input_ok,
                            submit = submit)

@app.route("/register", methods=['GET', 'POST'])
def register():
    '''
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    '''
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(username=form.username.data, 
                    email=form.email.data, 
                    phone=form.phone.data,
                    password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        form = LoginForm()
        return redirect(url_for('login',
                            form = form, 
                            input_ok = input_ok, 
                            input_error = input_error,
                            submit = submit))
    return render_template('register.html', 
                            form = form, 
                            input_ok = input_ok, 
                            input_error = input_error,
                            submit = submit)


@app.route("/main", methods=['GET', 'POST'])

def main():
    form = ParkingSpaceForm()
    if form.validate_on_submit():
        form = ParkingSpaceForm()
        parking_id=form.space_id.data
        user = current_user
        user.parking_space = parking_id
        user.call_time = datetime.today()
        user.calls += 1
        db.session.commit()
        return redirect (url_for('exit'))
    return render_template('main.html', 
                            form=form,
                            input_ok = input_main, 
                            input_error = input_error,
                            submit = submit)

@app.route("/api")
def api():
    objects = User.query.all()
    listing = {}
    listing['active'] = []
    for object in objects:
        d = {}
        d['ID'] = object.id
        d['TIME'] = object.call_time.strftime('%H %M %S')
        d['SPACE'] = object.parking_space
        d['PHONE'] = object.phone
        listing['active'].append(d)
    return listing

@app.route("/exit")
def exit():
    return render_template('exit.html')

if __name__ == '__main__':
    app.run(debug=True)
