from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
)


class SignUpForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=3, max=20)]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Sign Up')


class SignInForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
