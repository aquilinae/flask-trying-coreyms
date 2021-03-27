from flask_wtf import FlaskForm
from flask_wtf.file import (
    FileAllowed,
    FileField,
)
from flask_login import current_user
from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    ValidationError,
)
from app.models import User


class SignUpForm(FlaskForm):
    username = StringField(
        label='Username',
        validators=[DataRequired(), Length(min=3, max=20)]
    )
    email = StringField(
        label='Email',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        label='Password',
        validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        label='Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is taken. Please choose a different one')


class SignInForm(FlaskForm):
    email = StringField(
        label='Email',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        label='Password',
        validators=[DataRequired()]
    )
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class UpdateAccountForm(FlaskForm):
    username = StringField(
        label='Username',
        validators=[DataRequired(), Length(min=3, max=20)]
    )
    email = StringField(
        label='Email',
        validators=[DataRequired(), Email()]
    )
    picture = FileField(
        label='Update profile picture',
        validators=[FileAllowed(['jpg', 'png'])]
    )
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is taken. Please choose a different one')


class PostForm(FlaskForm):
    title = StringField(
        label='Title',
        validators=[DataRequired()]
    )
    content = TextAreaField(
        label='Content',
        validators=[DataRequired()]
    )
    submit = SubmitField(label='Post')


class RequestResetForm(FlaskForm):
    email = StringField(
        label='Email',
        validators=[DataRequired(), Email()]
    )
    submit = SubmitField('Request password reset')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is None:
            raise ValidationError('There is no accounnt with that email. Your must register first')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        label='Password',
        validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        label='Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Reset password')
