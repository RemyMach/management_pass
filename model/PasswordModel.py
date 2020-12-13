from app import db

class PasswordModel(db.Model):
    __tablename__ = 'password'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    password = db.Column(db.String())
    email = db.Column(db.String())

    def __init__(self, url, password, email):
        self.url = url
        self.password = password
        self.email = email