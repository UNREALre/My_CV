from flask import render_template, request, session, flash, redirect, url_for
from flask_babel import lazy_gettext as _l
from flask_login import current_user
from cvapp import app, db
from cvapp.helpers import get_settings, css_js_update_time
from cvapp.models import Education, Job, Skills, Certification, Portfolio, Feedback
from cvapp.forms import FeedbackForm
from cvapp.email import send_email


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    times = css_js_update_time(for_public=True)

    form = FeedbackForm()

    if form.validate_on_submit():
        msg = '<b>Имя</b>: {}<br><br><b>Email</b>: {}<br><br><b>Сообщение</b>:<br>{}'.format(
            form.name.data, form.email.data, form.message.data
        )
        send_email(_l('Сообщение с сайта Podrabinovich.RU'),
                   'noreply@podrabinovich.ru',
                   app.config['ADMINS'],
                   msg, msg)

        feedback = Feedback(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(feedback)
        db.session.commit()
        flash(_l('Сообщение было успешно отослано!'))

        return redirect(url_for('index', _anchor='form-flash'))

    lang = session.get('lang') if not request.args.get('lang') else request.args.get('lang')
    lang = 'ru' if not lang else lang
    settings = get_settings()
    schools = Education.query.order_by(Education.start_date.desc()).filter_by(language=lang.upper())
    jobs = Job.query.order_by(Job.start_date.desc()).filter_by(language=lang.upper())
    skills = Skills.query.all()
    certs = Certification.query.order_by(Certification.id.asc()).all()
    portfolio = Portfolio.query.order_by(Portfolio.order.asc()).all()

    return render_template('public/base.html',
                           form=form,
                           portfolio=portfolio,
                           certs=certs,
                           skills=skills,
                           jobs=jobs,
                           schools=schools,
                           settings=settings,
                           times=times
                           )
