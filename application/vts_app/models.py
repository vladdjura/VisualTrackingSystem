from datetime import datetime
from vts_app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    parking_space = db.Column(db.Integer, default = 0)
    registration_time = db.Column(db.DateTime, nullable=False, default=datetime.today()) #date-time of registration
    calls = db.Column(db.Integer, default = 0)
    call_time = db.Column(db.DateTime, nullable=False, default=datetime.today())
    status = db.Column(db.Integer, default = 0)
    colleague = db.Column(db.Integer, default = 0)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', status:'{self.status}', colleague: '{self.colleague}')"