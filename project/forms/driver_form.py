from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FloatField, IntegerField, BooleanField, HiddenField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional
from flask_wtf.file import FileRequired, FileAllowed

#####################
# Driver Forms      #
#####################

class DriverForm(FlaskForm):
    driver_id = StringField('Driver ID', validators=[DataRequired(), Length(min=2, max=100)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    status = SelectField('Status', choices=[('available', 'Available'), ('unavailable', 'Unavailable')])
    submit = SubmitField('Submit')