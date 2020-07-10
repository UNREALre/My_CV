import logging
import re
from logging.handlers import SMTPHandler
from flask import Flask, request, session
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_babel import Babel, lazy_gettext as _l
from flask_mail import Mail
from datetime import datetime
from jinja2 import evalcontextfilter, Markup, escape

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'
login.login_message = _l('Пожалуйста, авторизуйтесь, чтобы получить доступ к этой странице')

babel = Babel(app)

mail = Mail(app)


@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    elif not session.get('lang'):
        session['lang'] = request.accept_languages.best_match(app.config['LANGUAGES'])

    return session.get('lang')


@app.context_processor
def inject_now():
    """Injection now variable to all Jinja2 templates"""

    return {'now': datetime.utcnow()}


@app.context_processor
def inject_lang():
    lang = session.get('lang') if not request.args.get('lang') else request.args.get('lang')
    return {'lang': lang}


@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    """Converts newlines in text to HTML-tags"""

    value = re.sub(r'\r\n|\r|\n', '\n', value) # normalize newlines
    paras = re.split('\n{2,}', value)
    paras = [u'<p>%s</p>' % p.replace('\n', '<br />') for p in paras]
    paras = u'\n\n'.join(paras)
    return Markup(paras)


if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = () if app.config['MAIL_USE_TLS'] else None
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='webdevre@gmail.com',
            toaddrs=app.config['ADMINS'],
            subject='CV Error',
            credentials=auth,
            secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


from cvapp.routes import public, admin, errors
