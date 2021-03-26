import os
import secrets

from PIL import Image

from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)

from app import (
    app,
    bcrypt,
    db,
)
from app.forms import (
    SignInForm,
    SignUpForm,
    UpdateAccountForm,
)
from app.models import (
    User,
    Post,
)

POSTS = [
    {
        'author': 'ornichola',
        'title': 'First post',
        'content': 'Lorem ipsum',
        'date_posted': 'March 24, 2021',
    },
    {
        'author': 'not_ornichola',
        'title': 'Second post',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus id ornare lorem. Duis at imperdiet tortor, vel ullamcorper velit. Vivamus euismod ipsum et nibh consequat ultricies. Donec et tortor dui. Sed iaculis in tortor vitae ultrices. Aenean quis orci a tellus bibendum egestas ac nec neque. Cras viverra nunc in turpis lobortis porttitor. Suspendisse potenti. Praesent fringilla, urna id ullamcorper egestas, felis purus vestibulum sapien, sollicitudin facilisis dolor dui ac ligula. Donec sit amet risus id nisi viverra fringilla nec ac ligula.',
        'date_posted': 'March 25, 2021',
    }
]


@app.route('/')
def index():
    return render_template('index.html', posts=POSTS)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('sign_in'))
    return render_template('sign-up.html', title='Sign Up', form=form)


@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('sign-in.html', title='Sign In', form=form)


@app.route('/sign-out')
def sign_out():
    logout_user()
    return redirect(url_for('index'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', title='Account', image_file=image_file, form=form)
