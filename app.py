from flask import (
    Flask,
    render_template,
    url_for,
)


app = Flask(__name__, template_folder='templates')

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
@app.route('/home')
def home():
    return render_template('home.html', posts=POSTS)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


if __name__ == '__main__':
    app.run(debug=True)
