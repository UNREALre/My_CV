# -*- coding: utf-8 -*-
from flask import render_template, request, session, flash, redirect, url_for, Blueprint
from flask_babel import lazy_gettext as _l
from flask_login import current_user
import requests
from cvapp import app, db
from cvapp.helpers import get_settings, css_js_update_time
from cvapp.models import Education, Job, Skills, Certification, Portfolio, Feedback, Post, Category
from cvapp.forms import FeedbackForm
from cvapp.email import send_email

blueprint = Blueprint('public', __name__)


@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/index', methods=['GET', 'POST'])
def index():
    times = css_js_update_time(True)

    form = FeedbackForm()

    if form.validate_on_submit():
        rcp_info = {
            'secret': app.config['RECAPTCHA_SECRET'],
            'response': request.form['g-recaptcha-response']
        }
        captcha_resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=rcp_info)
        if not captcha_resp.json().get('success'):
            flash(_l('Кажется, Вы робот!'))
        else:
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

        return redirect(url_for('public.index', _anchor='form-flash'))

    lang = session.get('lang') if not request.args.get('lang') else request.args.get('lang')
    lang = 'ru' if not lang else lang
    settings = get_settings()
    schools = Education.query.order_by(Education.start_date.desc()).filter_by(language=lang.upper())
    jobs = Job.query.order_by(Job.start_date.desc()).filter_by(language=lang.upper())
    skills = Skills.query.all()
    certs = Certification.query.order_by(Certification.id.asc()).all()
    portfolio = Portfolio.query.order_by(Portfolio.order.asc()).all()

    return render_template('public/index.html',
                           form=form,
                           portfolio=portfolio,
                           certs=certs,
                           skills=skills,
                           jobs=jobs,
                           schools=schools,
                           settings=settings,
                           times=times
                           )


@blueprint.route('/blog')
def blog():
    times = css_js_update_time(True)
    settings = get_settings()

    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    prev_url = url_for('public.blog', page=posts.prev_num) if posts.has_prev else None
    next_url = url_for('public.blog', page=posts.next_num) if posts.has_next else None

    return render_template('public/blog.html',
                           posts=posts.items,
                           next_url=next_url,
                           prev_url=prev_url,
                           settings=settings,
                           times=times
                           )


@blueprint.route('/blog/<slug>')
def post(slug):
    times = css_js_update_time(True)
    settings = get_settings()
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('public/post.html',
                           post=post,
                           settings=settings,
                           times=times
                           )


@blueprint.route('/blog/category/<slug>')
def category(slug):
    times = css_js_update_time(True)
    settings = get_settings()
    category = Category.query.filter_by(slug=slug).first_or_404()

    return render_template('public/category.html',
                           posts=category.posts,
                           category=category,
                           settings=settings,
                           times=times)
