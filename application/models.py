from run import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    parking_space = db.Column(db.Integer, default = 0)
    registration = db.Column(db.String(19), default = None) #date-time of registration
    timestamp = db.Column(db.String(19), default = None)
    status = db.Column(db.Integer, default = 0)
    colleague = db.Column(db.Integer, default = 0)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"