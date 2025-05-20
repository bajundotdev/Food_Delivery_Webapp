from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FloatField, IntegerField, BooleanField, HiddenField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional
from flask_wtf.file import FileRequired, FileAllowed

########################
# Authentication Forms #
########################
class LoginForm(FlaskForm):
    username = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control"}
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    remember = BooleanField(
        'Remember Me',
        render_kw={"class": "form-check-input"}
    )
    submit = SubmitField(
        'Log In',
        render_kw={"class": "btn btn-primary"}
    )

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')