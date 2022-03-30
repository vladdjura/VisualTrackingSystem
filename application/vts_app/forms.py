from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, NumberRange, ValidationError
from vts_app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=8, max=12), Regexp('^\+', message='Phone number must starts with +')])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ParkingSpaceForm(FlaskForm):
    parking_id = IntegerField('parking_id', validators=[DataRequired(), NumberRange(min=1, max=14, message='parking space id takes labels from 1 to 14')])
    submit = SubmitField('Start Tracking')

class ExitForm(FlaskForm):
    submit = SubmitField('Stop Tracking')

class StoperForm(FlaskForm):
    password = IntegerField('Password', validators=[DataRequired()])
    user_id = IntegerField('User ID', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Stop Tracking')

class AdminForm(FlaskForm):
    password = IntegerField('Admin password', validators=[DataRequired()])
    ID = IntegerField('User_id', validators=[DataRequired(), NumberRange(min=1)])
    permission = IntegerField('Permission', validators=[NumberRange(min=0, max=1)])
    submit = SubmitField('Change Permission')

class DataForm(FlaskForm):
    password = PasswordField('Admin password', validators=[DataRequired()])
    submit = SubmitField('Download Data')
