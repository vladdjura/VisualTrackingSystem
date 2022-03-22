from vts_app.styles import input_ok, input_error, submit, input_main, error_main
from flask import render_template, redirect, url_for, flash
from vts_app import app, db, bcrypt
from vts_app.forms import RegistrationForm, LoginForm, ParkingSpaceForm, ExitForm, StoperForm, AdminForm
from vts_app.models import User
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/register", methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main')) 
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, 
                    email=form.email.data, 
                    phone=form.phone.data,
                    password=hashed_password)
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


@app.route('/', methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST']) 
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main')) 
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.colleague:
                login_user(user)
                return redirect(url_for('main'))
            return render_template('login.html', 
                            failed = True,
                            form = form, 
                            input_ok = input_ok, 
                            input_error = input_error,
                            submit = submit)
    return render_template('login.html', 
                            form = form, 
                            input_ok = input_ok, 
                            input_error = input_error,
                            submit = submit)


@app.route("/main", methods=['GET', 'POST'])
@login_required
def main():
    form = ParkingSpaceForm()
    if form.validate_on_submit():
        form = ParkingSpaceForm()
        parking_id=form.parking_id.data
        user = current_user
        user.parking_space = parking_id
        user.call_time = datetime.today()
        user.calls += 1
        user.status = 1
        db.session.commit()
        return redirect (url_for('exit'))
    return render_template('main.html', 
                            form=form,
                            input_ok = input_main, 
                            input_error = error_main,
                            submit = submit)


@app.route("/exit", methods=['GET', 'POST'])
@login_required
def exit():
    form = ExitForm()
    if form.validate_on_submit():
        user = current_user
        user.status = 0
        db.session.commit()  
        return redirect(url_for('main'))  
    user = current_user
    time = user.call_time.strftime('%Hh : %Mm : %Ss')
    space = user.parking_space
    username = user.username
    return render_template('exit.html',
                            form = form,
                            time = time,
                            space = space,
                            username = username,
                            submit = submit)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))   

@app.route("/api")
def api():
    objects = User.query.all()
    listing = {}
    listing['active'] = []
    for object in objects:
        if object.colleague:
            d = {}
            d['ID'] = object.id
            d['TIME'] = object.call_time.strftime('%H %M %S')
            d['SPACE'] = object.parking_space
            d['PHONE'] = object.phone
            d['STATUS'] = object.status
            listing['active'].append(d)
    return listing

@app.route('/stoper', methods = ['GET','POST'])
def stoper():
    form = StoperForm()
    if form.validate_on_submit():
        form = StoperForm()
        admin = User.query.get(1)
        if bcrypt.check_password_hash(admin.password, str(form.password.data)):
            user = User.query.get(form.user_id.data)
            user.status = 0
            db.session.commit()
            flash('Status successfully changed')   
    return render_template('stoper.html',
                            form = form,
                            input_ok = input_ok, 
                            input_error = input_error,
                            submit = submit)


@app.route('/admin', methods = ['GET','POST'])
def admin():
    form = AdminForm()
    users = {'active':[]}
    complete = User.query.all()
    for user in complete:
        user_dict = {}
        user_dict['id'] = user.id
        user_dict['registration'] = user.registration_time.strftime("%Y/%m/%d %H:%M:%S")
        user_dict['email'] = user.email
        user_dict['permission'] = user.colleague
        users['active'].append(user_dict)
        users['active'] = sorted(users['active'], key=lambda x: x['registration'], reverse=True)
    if form.validate_on_submit():
        form = AdminForm()
        admin = User.query.get(1)
        if bcrypt.check_password_hash(admin.password, str(form.password.data)):
            user=User.query.get(form.ID.data)
            user.colleague=form.permission.data
            db.session.commit()
    return render_template('admin.html',
                            users = users,
                            form = form,
                            input_main = input_main, 
                            input_ok = input_ok, 
                            input_error = input_error,
                            error_main = error_main,
                            submit = submit)

