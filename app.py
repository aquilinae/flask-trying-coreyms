from config import SECRET_KEY
from datetime import datetime
from flask import (
    flash,
    Flask,
    redirect,
    render_template,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from forms import (
    SignInForm,
    SignUpForm,
)


app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


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
    form = SignUpForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('sign-up.html', title='Sign Up', form=form)


@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm()
    if form.validate_on_submit():
        flash('You have been logged in', 'success')
        return redirect(url_for('index'))
    return render_template('sign-in.html', title='Sign In', form=form)


if __name__ == '__main__':
    app.run(debug=True)
