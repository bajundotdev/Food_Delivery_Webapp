from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FloatField, IntegerField, BooleanField, HiddenField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional
from flask_wtf.file import FileRequired, FileAllowed

class AddToCartForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, max=20)])
    product_id = HiddenField('Product ID')
    submit = SubmitField('Add to Cart')

class CheckoutForm(FlaskForm):
    address = StringField('Shipping Address', validators=[DataRequired()])
    payment_method = SelectField('Payment Method', choices=[('cash', 'Cash'), ('credit', 'Credit Card')], validators=[DataRequired()])
    submit = SubmitField('Place Order')
