from cvapp import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


@login.user_loader
def load_user(id):
    """Используется Flask-login-ом, чтобы получить информацию из БД о пользователе по его id"""
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Settings(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    param_name = db.Column(db.String(100), index=True, unique=True)
    param_value = db.Column(db.Text)

    def __repr__(self):
        return '<Setting {} = {}>'.format(self.param_name, self.param_value)


class Education(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    start_date = db.Column(db.DateTime, default=datetime.utcnow())
    end_date = db.Column(db.DateTime)
    name = db.Column(db.String(200), index=True)
    description = db.Column(db.Text)
    language = db.Column(db.String(2))

    def __repr__(self):
        return '<Education #{}. "{}". From {} to {}.>'.format(self.id, self.name, self.start_date, self.end_date)


class Job(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    start_date = db.Column(db.DateTime, default=datetime.utcnow())
    end_date = db.Column(db.DateTime)
    name = db.Column(db.String(200), index=True)
    description = db.Column(db.Text)
    language = db.Column(db.String(2))

    def __repr__(self):
        return '<Job #{}. "{}". From {} to {}.>'.format(self.id, self.name, self.start_date, self.end_date)


class Skills(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100))
    name_en = db.Column(db.String(100))
    description = db.Column(db.String(100))
    description_en = db.Column(db.String(100))
    percentage = db.Column(db.Integer)
    type = db.Column(db.String(10))

    def __repr__(self):
        return '<Skills #{}. {} - {}>'.format(self.id, self.name, self.description)


class Certification(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(500))
    link = db.Column(db.String(500))
    image = db.Column(db.String(200))

    def __repr__(self):
        return '<Certification #{}. {}>'.format(self.id, self.name)


class Portfolio(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    order = db.Column(db.Integer)
    category = db.Column(db.String(100))
    category_en = db.Column(db.String(100))
    name = db.Column(db.String(200))
    name_en = db.Column(db.String(200))
    description = db.Column(db.Text)
    description_en = db.Column(db.Text)
    image = db.Column(db.String(200))
    link = db.Column(db.String(200))

    def __repr__(self):
        return '<Portfolio #{}. {}>'.format(self.id, self.name)


class Feedback(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(100))
    message = db.Column(db.Text)

    def __repr__(self):
        return '<Feedback #{} from {}.>'.format(self.id, self.name)
