# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from flask_babel import lazy_gettext as _l
from wtforms import (StringField, PasswordField, BooleanField, SubmitField,
                     TextAreaField, SelectField)
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional
from cvapp.models import User, Category


class CvBaseForm(FlaskForm):
    class Meta:
        locales = ['ru']


class LoginForm(CvBaseForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(CvBaseForm):
    """Just for practice. Class doesn't need to be within current project."""

    username = StringField('Логин', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Данный логин уже занят!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Данный E-mail уже занят!')


class SettingsForm(CvBaseForm):
    param_name = StringField(_l('Наименование параметра'), validators=[DataRequired()])
    param_value = TextAreaField(_l('Значение параметра'), validators=[Optional()])
    param_file = FileField(_l('Загрузить файл'), validators=[Optional()])
    submit = SubmitField(_l('Сохранить'))


class EducationForm(CvBaseForm):
    name = StringField(_l('Наименование'), validators=[DataRequired()])
    description = TextAreaField(_l('Описание'), validators=[DataRequired()])
    start_date = DateField(_l('Дата начала'), validators=[DataRequired()])
    end_date = DateField(_l('Дата окончания'), validators=[Optional()])
    language = SelectField(_l('Язык'), choices=[('RU', 'RU'), ('EN', 'EN')])
    submit = SubmitField(_l('Сохранить'))


class JobForm(CvBaseForm):
    name = StringField(_l('Наименование'), validators=[DataRequired()])
    description = TextAreaField(_l('Описание'), validators=[DataRequired()])
    start_date = DateField(_l('Дата начала'), validators=[DataRequired()])
    end_date = DateField(_l('Дата окончания'), validators=[Optional()])
    language = SelectField(_l('Язык'), choices=[('RU', 'RU'), ('EN', 'EN')])
    submit = SubmitField(_l('Сохранить'))


class SkillForm(CvBaseForm):
    name = StringField(_l('Наименование'), validators=[DataRequired()])
    name_en = StringField(_l('Наименование на английском'), validators=[Optional()])
    description = StringField(_l('Описание'), validators=[DataRequired()])
    description_en = StringField(_l('Описание на английском'), validators=[Optional()])
    percentage = StringField(_l('Проценты'), validators=[DataRequired()])
    type = SelectField(_l('Тип'), choices=[('hard', 'hard'), ('soft', 'soft'), ('lang', 'lang')])
    submit = SubmitField(_l('Сохранить'))


class CertForm(CvBaseForm):
    name = StringField(_l('Наименование'), validators=[DataRequired()])
    link = StringField(_l('Ссылка'), validators=[Optional()])
    image_file = FileField(_l('Файл'), validators=[Optional()])
    submit = SubmitField(_l('Сохранить'))


class PortfolioForm(CvBaseForm):
    order = StringField(_l('Порядок вывода'), validators=[DataRequired()])
    category = StringField(_l('Категория'), validators=[DataRequired()])
    category_en = StringField(_l('Категория на английском'), validators=[DataRequired()])
    name = StringField(_l('Наименование'), validators=[DataRequired()])
    name_en = StringField(_l('Наименование на английском'), validators=[DataRequired()])
    description = TextAreaField(_l('Описание'), validators=[DataRequired()])
    description_en = TextAreaField(_l('Описание на английском'), validators=[DataRequired()])
    link = StringField(_l('Ссылка на проект'), validators=[Optional()])
    image_file = FileField(_l('Изображение'), validators=[Optional()])
    submit = SubmitField(_l('Сохранить'))


class FeedbackForm(CvBaseForm):
    name = StringField(_l('Имя'), validators=[DataRequired()])
    email = StringField(_l('E-mail'), validators=[DataRequired(), Email()])
    message = TextAreaField(_l('Сообщение'), validators=[DataRequired()])
    submit = SubmitField(_l('Отправить сообщение'))


class BlogPostForm(CvBaseForm):
    name = StringField(_l('Заглавие'), validators=[DataRequired()])
    slug = StringField(_l('Slug'), validators=[DataRequired()])
    description = TextAreaField(_l('Description'), validators=[Optional()])
    keywords = TextAreaField(_l('Keywords'), validators=[Optional()])
    text = TextAreaField(_l('Текст'), validators=[DataRequired()])
    categories = QuerySelectMultipleField(_l('Категории'),
                                          query_factory=lambda: Category.query.order_by(Category.name.asc()),
                                          get_label='name', validators=[DataRequired()])
    submit = SubmitField(_l('Сохранить'))


class BlogCategoryForm(CvBaseForm):
    name = StringField(_l('Наименование'), validators=[DataRequired()])
    slug = StringField(_l('Slug'), validators=[DataRequired()])
    submit = SubmitField(_l('Сохранить'))
