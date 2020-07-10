from flask import render_template
from flask_babel import lazy_gettext as _l
from cvapp import app, db


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', content=_l('Извините, страница не найдена.'), full_error=error), 404


@app.errorhandler(500)
def not_found_error(error):
    db.session.rollback()
    return render_template('error.html', content=_l('Извините, что-то пошло не так'), full_error=error), 500
