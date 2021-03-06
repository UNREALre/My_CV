# -*- coding: utf-8 -*-
import os
from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import current_user, login_required, logout_user, login_user
from cvapp import app, db
from cvapp.models import (User, Settings, Education, Job, Skills, Certification, Portfolio, Feedback,
                          Post, Category)
from cvapp.forms import (LoginForm, RegistrationForm, SettingsForm, EducationForm,
                         JobForm, SkillForm, CertForm, PortfolioForm, BlogPostForm, BlogCategoryForm)
from cvapp.helpers import css_js_update_time, save_uploaded_file
from config import project_root

blueprint = Blueprint('admin', __name__)


@blueprint.route('/')
@login_required
def admin():
    static_times = css_js_update_time()
    return render_template('admin/index.html', times=static_times)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    static_times = css_js_update_time()

    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверный логин/пароль')
            return redirect(url_for('admin.login'))

        login_user(user, remember=form.remember_me.data)
        # check if user comes from any protected non-anonymous page to return him where he wanted to be before login
        next_page = request.args.get('next') or url_for('admin.index')
        return redirect(next_page)

    return render_template('admin/login.html', title='Авторизация', form=form, times=static_times)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """Just for testing purposes. No need to have this view-function for this project."""

    static_times = css_js_update_time()

    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Поздравляем, Вы успешно зарегистрировались!')
        return redirect(url_for('admin.login'))

    return render_template('admin/register.html', title='Регистрация', form=form, times=static_times)


@blueprint.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    static_times = css_js_update_time()

    settings = Settings.query.all()
    form = SettingsForm()

    if form.validate_on_submit():
        if form.param_file.data:
            form.param_value.data = save_uploaded_file(app.config['UPLOAD_FOLDER'], form.param_file)

        setting_item = Settings(param_name=form.param_name.data, param_value=form.param_value.data)
        db.session.add(setting_item)
        db.session.commit()
        return redirect(url_for('admin.settings'))

    return render_template('admin/settings.html', form=form, settings=settings, times=static_times)


@blueprint.route('/edit-settings/<setting_id>', methods=['POST'])
@login_required
def edit_settings(setting_id):
    # setting = Settings.query.get(setting_id)
    # if not setting:
    #    raise ValueError('No object with such ID within database!')
    # Let's write more beautiful solution

    setting = Settings.query.filter_by(id=setting_id).first_or_404()

    form = SettingsForm()
    if form.validate_on_submit():
        if form.param_file.data:
            form.param_value.data = save_uploaded_file(app.config['UPLOAD_FOLDER'], form.param_file)

        setting.param_name = form.param_name.data
        setting.param_value = form.param_value.data
        db.session.add(setting)
        db.session.commit()

    return redirect(url_for('admin.settings'))


@blueprint.route('/delete-settings/<setting_id>', methods=['POST'])
@login_required
def delete_settings(setting_id):
    # One line alternative
    # Settings.query.filter_by(id=setting_id).delete()

    setting = Settings.query.get(setting_id)
    if not setting:
        raise ValueError('No object with such ID within database!')

    if os.path.isfile(os.path.join(project_root, app.config['UPLOAD_FOLDER'], setting.param_value)):
        os.remove(os.path.join(project_root, app.config['UPLOAD_FOLDER'], setting.param_value))

    db.session.delete(setting)
    db.session.commit()

    return redirect(url_for('admin.settings'))


@blueprint.route('/education', methods=['GET', 'POST'])
@login_required
def education():
    times = css_js_update_time()

    schools = Education.query.all()
    form = EducationForm()

    if form.validate_on_submit():
        school = Education(name=form.name.data, description=form.description.data,
                           start_date=form.start_date.data, end_date=form.end_date.data, language=form.language.data)

        db.session.add(school)
        db.session.commit()

        return redirect(url_for('admin.education'))

    return render_template('admin/education.html', form=form, list=schools, times=times)


@blueprint.route('/edit-education/<school_id>', methods=['POST'])
@login_required
def edit_education(school_id):
    school = Education.query.filter_by(id=school_id).first_or_404()

    form = EducationForm()
    if form.validate_on_submit():
        school.name = form.name.data
        school.description = form.description.data
        school.start_date = form.start_date.data
        school.end_date = form.end_date.data
        school.language = form.language.data

        db.session.add(school)
        db.session.commit()

        return redirect(url_for('admin.education'))


@blueprint.route('/delete-education/<school_id>', methods=['POST'])
@login_required
def delete_education(school_id):
    school = Education.query.filter_by(id=school_id).first_or_404()

    db.session.delete(school)
    db.session.commit()

    return redirect(url_for('admin.education'))


@blueprint.route('/jobs', methods=['GET', 'POST'])
@login_required
def jobs():
    times = css_js_update_time()

    jobs = Job.query.all()

    form = JobForm()
    if form.validate_on_submit():
        job = Job(name=form.name.data, description=form.description.data,
                  start_date=form.start_date.data, end_date=form.end_date.data, language=form.language.data)
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('admin.jobs'))

    return render_template('admin/jobs.html', list=jobs, form=form, times=times)


@blueprint.route('/edit-job/<job_id>', methods=['POST'])
@login_required
def edit_job(job_id):
    form = JobForm()
    job = Job.query.filter_by(id=job_id).first_or_404()
    if form.validate_on_submit():
        job.name = form.name.data
        job.description = form.description.data
        job.start_date = form.start_date.data
        job.end_date = form.end_date.data
        job.language = form.language.data

        db.session.add(job)
        db.session.commit()

    return redirect(url_for('admin.jobs'))


@blueprint.route('/delete-job/<job_id>', methods=['POST'])
@login_required
def delete_job(job_id):
    job = Job.query.filter_by(id=job_id).first_or_404()
    db.session.delete(job)
    db.session.commit()

    return redirect(url_for('admin.jobs'))


@blueprint.route('/skills', methods=['GET', 'POST'])
@login_required
def skills():
    times = css_js_update_time()
    form = SkillForm()
    skills = Skills.query.all()

    if form.validate_on_submit():
        skill = Skills(name=form.name.data, name_en=form.name_en.data,
                       description=form.description.data, description_en=form.description_en.data,
                       percentage=form.percentage.data, type=form.type.data)
        db.session.add(skill)
        db.session.commit()

        return redirect(url_for('admin.skills'))

    return render_template('admin/skills.html', list=skills, form=form, times=times)


@blueprint.route('/edit-skill/<skill_id>', methods=['POST'])
@login_required
def edit_skill(skill_id):
    skill = Skills.query.filter_by(id=skill_id).first_or_404()
    form = SkillForm()
    if form.validate_on_submit():
        skill.name = form.name.data
        skill.name_en = form.name_en.data
        skill.description = form.description.data
        skill.description_en = form.description_en.data
        skill.percentage = form.percentage.data
        skill.type = form.type.data

        db.session.add(skill)
        db.session.commit()

    return redirect(url_for('admin.skills'))


@blueprint.route('/delete-skill/<skill_id>', methods=['POST'])
@login_required
def delete_skill(skill_id):
    skill = Skills.query.filter_by(id=skill_id).first_or_404()
    db.session.delete(skill)
    db.session.commit()

    return redirect(url_for('admin.skills'))


@blueprint.route('/certs', methods=['GET', 'POST'])
@login_required
def certs():
    times = css_js_update_time()
    certs = Certification.query.all()
    form = CertForm()

    if form.validate_on_submit():
        cert = Certification(name=form.name.data, link=form.link.data)
        if form.image_file.data:
            cert.image = save_uploaded_file(app.config['UPLOAD_FOLDER'], form.image_file)

        db.session.add(cert)
        db.session.commit()

        return redirect(url_for('admin.certs'))

    return render_template('admin/certs.html', list=certs, form=form, times=times)


@blueprint.route('/edit-cert/<cert_id>', methods=['POST'])
@login_required
def edit_cert(cert_id):
    cert = Certification.query.filter_by(id=cert_id).first_or_404()
    form = CertForm()
    if form.validate_on_submit():
        cert.name = form.name.data
        cert.link = form.link.data
        if form.image_file.data:
            if cert.image:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], cert.image))
            cert.image = save_uploaded_file(app.config['UPLOAD_FOLDER'], form.image_file)

        db.session.add(cert)
        db.session.commit()

    return redirect(url_for('admin.certs'))


@blueprint.route('/delete-cert/<cert_id>', methods=['POST'])
@login_required
def delete_cert(cert_id):
    cert = Certification.query.filter_by(id=cert_id).first_or_404()
    if cert.image:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], cert.image))
    db.session.delete(cert)
    db.session.commit()

    return redirect(url_for('admin.certs'))


@blueprint.route('/portfolio', methods=['GET', 'POST'])
@login_required
def portfolio():
    times = css_js_update_time()
    form = PortfolioForm()
    portfolio_list = Portfolio.query.order_by(Portfolio.order.asc()).all()

    if form.validate_on_submit():
        portfolio = Portfolio(name=form.name.data, name_en=form.name_en.data,
                              category=form.category.data, category_en=form.category_en.data,
                              description=form.description.data, description_en=form.description_en.data,
                              link=form.link.data, order=form.order.data)
        if form.image_file.data:
            portfolio.image = save_uploaded_file(app.config['UPLOAD_FOLDER'], form.image_file)

        db.session.add(portfolio)
        db.session.commit()

        return redirect(url_for('admin.portfolio'))

    return render_template('admin/portfolio.html', list=portfolio_list, form=form, times=times)


@blueprint.route('/edit-portfolio/<portfolio_id>', methods=['POST'])
@login_required
def edit_portfolio(portfolio_id):
    portfolio = Portfolio.query.filter_by(id=portfolio_id).first_or_404()
    form = PortfolioForm()
    if form.validate_on_submit():
        if form.image_file.data:
            if portfolio.image:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], portfolio.image))
            portfolio.image = save_uploaded_file(app.config['UPLOAD_FOLDER'], form.image_file)
        portfolio.name = form.name.data
        portfolio.name_en = form.name_en.data
        portfolio.description = form.description.data
        portfolio.description_en = form.description_en.data
        portfolio.category = form.category.data
        portfolio.category_en = form.category_en.data
        portfolio.link = form.link.data
        portfolio.order = form.order.data

        db.session.add(portfolio)
        db.session.commit()

    return redirect(url_for('admin.portfolio'))


@blueprint.route('/delete-portfolio/<portfolio_id>', methods=['POST'])
@login_required
def delete_portfolio(portfolio_id):
    portfolio = Portfolio.query.filter_by(id=portfolio_id).first_or_404()
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], portfolio.image))
    db.session.delete(portfolio)
    db.session.commit()

    return redirect(url_for('admin.portfolio'))


@blueprint.route('/feedback')
@login_required
def feedback():
    times = css_js_update_time()
    emails = Feedback.query.order_by(Feedback.id.asc()).all()

    return render_template('admin/feedback.html', list=emails, times=times)


@blueprint.route('/delete-feedback/<feedback_id>', methods=['POST'])
@login_required
def delete_feedback(feedback_id):
    feedback = Feedback.query.filter_by(id=feedback_id).first_or_404()
    db.session.delete(feedback)
    db.session.commit()
    return redirect(url_for('admin.feedback'))


@blueprint.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
    times = css_js_update_time()
    posts = Post.query.order_by(Post.date.desc()).all()
    form = BlogPostForm()
    if form.validate_on_submit():
        post = Post(name=form.name.data, slug=form.slug.data,
                    description=form.description.data, keywords=form.keywords.data,
                    text=form.text.data, categories=form.categories.data)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('admin.posts'))

    return render_template('admin/posts.html', list=posts, form=form, times=times)


@blueprint.route('/edit-post/<post_id>', methods=['POST'])
@login_required
def edit_post(post_id):
    form = BlogPostForm()
    if form.validate_on_submit():
        post = Post.query.filter_by(id=post_id).first_or_404()
        post.name = form.name.data
        post.slug = form.slug.data
        post.description = form.description.data
        post.keywords = form.keywords.data
        post.text = form.text.data
        post.categories = form.categories.data
        db.session.add(post)
        db.session.commit()

    return redirect(url_for('admin.posts'))


@blueprint.route('/delete-post/<post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('admin.posts'))


@blueprint.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    times = css_js_update_time()
    form = BlogCategoryForm()
    categories = Category.query.order_by(Category.name.asc()).all()
    if form.validate_on_submit():
        category = Category(name=form.name.data, slug=form.slug.data)
        db.session.add(category)
        db.session.commit()

        return redirect(url_for('admin.categories'))

    return render_template('admin/categories.html', list=categories, form=form, times=times)


@blueprint.route('/edit-category/<category_id>', methods=['POST'])
@login_required
def edit_category(category_id):
    form = BlogCategoryForm()
    if form.validate_on_submit():
        category = Category.query.filter_by(id=category_id).first_or_404()
        category.name = form.name.data
        category.slug = form.slug.data
        db.session.add(category)
        db.session.commit()

    return redirect(url_for('admin.categories'))


@blueprint.route('/delete-category/<category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.filter_by(id=category_id).first_or_404()
    db.session.delete(category)
    db.session.commit()

    return redirect(url_for('admin.categories'))
