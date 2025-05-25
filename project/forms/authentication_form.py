from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FloatField, IntegerField, BooleanField, HiddenField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional
from flask_wtf.file import FileRequired, FileAllowed

########################
# Authentication Forms #
########################
class LoginForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    #remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    fullname = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone_number = StringField('Name', validators=[DataRequired(), Length(min=2, max=14)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    #address
    label = StringField('Lable', validators=[DataRequired(), Length(min=2, max=100)])
    address_line1 = StringField('Address Line 1', validators=[DataRequired(), Length(min=2, max=100)])
    address_line2 = StringField('Address Line 2', validators=[DataRequired(), Length(min=2, max=100)])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=100)])
    state = StringField('State', validators=[DataRequired(), Length(min=2, max=100)])
    postal_code = StringField('Postal Code', validators=[DataRequired(), Length(min=2, max=100)])
    country = StringField('Coutry', validators=[DataRequired(), Length(min=2, max=100)])
    ########
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class DriverRegistrationForm(FlaskForm):
    fullname = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone_number = StringField('Name', validators=[DataRequired(), Length(min=2, max=14)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    vehicle_type = StringField('Vehicle Type', validators=[DataRequired(), Length(min=2, max=100)])
    vehicle_plate = StringField('Vehicle Plate', validators=[DataRequired(), Length(min=2, max=100)])
    license_number = StringField('License Number', validators=[DataRequired(), Length(min=2, max=100)])
    #address
    label = StringField('Lable', validators=[DataRequired(), Length(min=2, max=100)])
    address_line1 = StringField('Address Line 1', validators=[DataRequired(), Length(min=2, max=100)])
    address_line2 = StringField('Address Line 2', validators=[DataRequired(), Length(min=2, max=100)])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=100)])
    state = StringField('State', validators=[DataRequired(), Length(min=2, max=100)])
    postal_code = StringField('Postal Code', validators=[DataRequired(), Length(min=2, max=100)])
    country = StringField('Coutry', validators=[DataRequired(), Length(min=2, max=100)])
    ########
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')