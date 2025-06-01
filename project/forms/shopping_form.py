from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FloatField, IntegerField, BooleanField, HiddenField, FileField, RadioField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional, InputRequired
from flask_wtf.file import FileRequired, FileAllowed

#####################
# Shopping Forms    #
#####################

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Search')

class CartForm(FlaskForm):
    product_id = HiddenField('Product ID')
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, max=20)], default=1)
    submit = SubmitField('Add to Cart')

class OrderForm(FlaskForm):
    address = SelectField('Delivery Address', validators=[DataRequired()])
    payment_method = SelectField('Payment Method', 
                               choices=[
                                   ('cash', 'Cash on Delivery'),
                                   ('credit_card', 'Credit Card'),
                                   ('debit_card', 'Debit Card')
                               ])
    notes = TextAreaField('Order Notes', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Place Order')

class CheckoutForm(FlaskForm):
    fullname = StringField("fullname", validators = [DataRequired(), Length(min=2, max=100)])
    phone = StringField("phone", validators = [DataRequired(), Length(min=2, max=100)])
    email = EmailField('email', validators=[DataRequired(), Email()])
    address = StringField("address", validators = [DataRequired(), Length(min=2, max=100)])
    notes = TextAreaField("Delivery Instructions")
    payment_method = RadioField('Choose an option:', choices=[('Credit Card', 'Credit Card'), ('Debit Card', 'Debit Card'), ('Cash', 'Cash')])
    shippingMethod = RadioField('Choose an option:', choices=[('Standard', 'Standard Delivery - Free'), ('Express', 'Express Delivery - $5.99')])
    packagingMethod = RadioField('Choose an option:', choices=[('Eco-Friendly', 'Eco-Friendly Packaging - Free'), ('Standard', 'Standard Packaging - $2.99'), ('Discreet and Confidential', 'Discreet and Confidential Packaging - $5.99')])
    submit = SubmitField("Place Order")