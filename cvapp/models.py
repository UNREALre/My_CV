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
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Settings(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    param_name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    param_value = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Setting {} = {}>'.format(self.param_name, self.param_value)


class Education(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    start_date = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    name = db.Column(db.String(200), index=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(2), nullable=False)

    def __repr__(self):
        return '<Education #{}. "{}". From {} to {}.>'.format(self.id, self.name, self.start_date, self.end_date)


class Job(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    start_date = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    name = db.Column(db.String(200), index=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(2), nullable=False)

    def __repr__(self):
        return '<Job #{}. "{}". From {} to {}.>'.format(self.id, self.name, self.start_date, self.end_date)


class Skills(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(100), nullable=False)
    description_en = db.Column(db.String(100), nullable=True)
    percentage = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<Skills #{}. {} - {}>'.format(self.id, self.name, self.description)


class Certification(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    link = db.Column(db.String(500), nullable=True)
    image = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return '<Certification #{}. {}>'.format(self.id, self.name)


class Portfolio(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    order = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    category_en = db.Column(db.String(100), nullable=True)
    name = db.Column(db.String(200), nullable=False)
    name_en = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=False)
    description_en = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(200), nullable=True)
    link = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return '<Portfolio #{}. {}>'.format(self.id, self.name)


class Feedback(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Feedback #{} from {}.>'.format(self.id, self.name)


post_categories = db.Table('post_categories',
                           db.Column('post_id', db.BigInteger, db.ForeignKey('post.id')),
                           db.Column('category_id', db.BigInteger, db.ForeignKey('category.id'))
                           )


class Category(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False)


class Post(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    keywords = db.Column(db.Text, nullable=True)
    text = db.Column(db.Text, nullable=False)
    categories = db.relationship(
        'Category', secondary=post_categories, lazy='subquery', backref=db.backref('posts', lazy=True)
    )
    date = db.Column(db.DateTime, default=datetime.utcnow())
