from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FloatField, IntegerField, BooleanField, HiddenField, FileField, RadioField
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
    """Form for user checkout."""
    fullname = StringField("Full Name", validators = [InputRequired()])
    phone = StringField("Your surname", validators = [InputRequired()])
    email = StringField("Your email", validators = [InputRequired(), Email()])
    address = StringField("Your phone number", validators = [InputRequired()])
    notes = StringField("Delivery Instructions", validators = [InputRequired()])
    payment_method = RadioField('Choose an option:', choices=[('option1', 'Credit Card'), ('option2', 'Debit Card'), ('option3', 'Cash on Delivery')], validators=[DataRequired()])
    submit = SubmitField("Place Order")