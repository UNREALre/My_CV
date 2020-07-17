import os
import confuse

project_root = os.path.dirname(os.path.abspath(__file__))
os.environ["CVDIR"] = project_root
appConfig = confuse.Configuration('CV')


class Config:
    # The Flask-WTF extension uses secret key it to protect web forms
    SECRET_KEY = appConfig['app']['secret'].get() or 'some-default-value'

    # Flash-SQLAlchemy config params
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(
        appConfig['db']['user'].get(), appConfig['db']['pass'].get(),
        appConfig['db']['host'].get(), appConfig['db']['name'].get())
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LANGUAGES = ['en', 'ru']

    MAIL_SERVER = appConfig['mail']['host'].get()
    MAIL_PORT = int(appConfig['mail']['port'].get() or 25)
    MAIL_USE_TLS = True
    MAIL_USERNAME = appConfig['mail']['user'].get()
    MAIL_PASSWORD = appConfig['mail']['pass'].get()
    ADMINS = ['avpmanager@gmail.com']

    UPLOAD_FOLDER = 'cvapp/static/uploads'
    UPLOAD_WEB_PATH = '/static/uploads'

    POSTS_PER_PAGE = int(appConfig['blog']['per_page'].get())

    # Disable cache
    # TEMPLATES_AUTO_RELOAD = True
    # SEND_FILE_MAX_AGE_DEFAULT = 0
