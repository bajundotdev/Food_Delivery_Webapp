from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FloatField, IntegerField, BooleanField, HiddenField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional
from flask_wtf.file import FileRequired, FileAllowed

###################
# Authentication Forms
###################
class LoginForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

###################
# Customer Forms
###################
class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    password = PasswordField('Password', validators=[Optional(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Update Profile')

class UserAddressForm(FlaskForm):
    street = StringField('Street Address', validators=[DataRequired(), Length(min=5, max=200)])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=100)])
    state = StringField('State/Province', validators=[DataRequired(), Length(min=2, max=100)])
    postal_code = StringField('Postal Code', validators=[DataRequired(), Length(min=4, max=10)])
    country = StringField('Country', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Save Address')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=2, max=100)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Send Message')

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], coerce=int)
    comment = TextAreaField('Comment', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Submit Review')

###################
# Shopping Forms
###################
class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Search')

class CartForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, max=20)])
    product_id = HiddenField('Product ID')
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

###################
# Admin Forms
###################
class AdminUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[
        ('customer', 'Customer'),
        ('admin', 'Admin'),
        ('driver', 'Delivery Driver'),
        ('restaurant_manager', 'Restaurant Manager')
    ])
    submit = SubmitField('Update User')

class AdminSearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired(), Length(min=2, max=100)])
    entity_type = SelectField('Type', choices=[
        ('all', 'All'),
        ('users', 'Users'),
        ('orders', 'Orders'),
        ('products', 'Products'),
        ('restaurants', 'Restaurants')
    ])
    submit = SubmitField('Search')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=1000)])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0.01)])
    category = SelectField('Category', validators=[DataRequired()])
    restaurant_id = SelectField('Restaurant', validators=[DataRequired()])
    image = FileField('Product Image', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    submit = SubmitField('Save Product')

class RestaurantForm(FlaskForm):
    name = StringField('Restaurant Name', validators=[DataRequired(), Length(min=2, max=100)])
    address = StringField('Address', validators=[DataRequired(), Length(min=5, max=200)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    website = StringField('Website', validators=[Optional(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=1000)])
    image = FileField('Restaurant Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    role = HiddenField('Role', default='restaurant_manager') 
    submit = SubmitField('Save Restaurant')

###################
# Driver Forms
###################
class DriverForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    status = SelectField('Status', choices=[('available', 'Available'), ('unavailable', 'Unavailable')])
    role = HiddenField('Role', default='driver') 
    submit = SubmitField('Submit')
