
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FloatField, IntegerField, BooleanField, HiddenField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional
from flask_wtf.file import FileRequired, FileAllowed

class CreateOrderForm(FlaskForm):
    customer = SelectField('Customer', validators=[DataRequired()])
    product = SelectField('Product', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    delivery_address = StringField('Delivery Address', validators=[DataRequired()])
    payment_method = SelectField('Payment Method', choices=[('credit_card', 'Credit Card'), ('debit_card', 'Debit Card'), ('cash', 'Cash on Delivery')], validators=[DataRequired()])
    special_instructions = TextAreaField('Special Instructions', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Create Order')