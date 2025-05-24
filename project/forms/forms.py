from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, TextAreaField, 
    SelectField, FloatField, IntegerField, BooleanField, 
    HiddenField, FileField
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, 
    NumberRange, Optional, ValidationError
)
from flask_wtf.file import FileAllowed
from project.models import User

class BaseUserForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=10, max=200)])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

class RegistrationForm(BaseUserForm):
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match')
    ])
    role = SelectField('Account Type', choices=[
        ('customer', 'Customer'),
        ('driver', 'Driver')
    ], validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Change Password')

class AdminUserForm(BaseUserForm):
    is_super_admin = BooleanField('Super Admin Privileges')
    submit = SubmitField('Save Admin')

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired(), Length(min=2, max=100)])
    search_type = SelectField('Search Type', choices=[
        ('products', 'Products'),
        ('users', 'Users'),
        ('orders', 'Orders')
    ], default='products')
    submit = SubmitField('Search')

class ProductForm(FlaskForm):
    product_id = StringField('Product ID', validators=[DataRequired(), Length(min=2, max=100)])
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[
        DataRequired(), 
        Length(min=10, max=500)
    ])
    price = FloatField('Price', validators=[
        DataRequired(),
        NumberRange(min=0.01, message='Price must be positive')
    ])
    stock = IntegerField('Initial Stock', validators=[
        DataRequired(),
        NumberRange(min=0, message='Stock cannot be negative')
    ])
    category = SelectField('Category', choices=[
        ('food', 'Food'),
        ('beverage', 'Beverage'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    image = FileField('Product Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Only JPEG/PNG images allowed')
    ])
    submit = SubmitField('Save Product')

class CartOperationForm(FlaskForm):
    product_id = HiddenField(validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[
        DataRequired(),
        NumberRange(min=1, max=20, message='Quantity must be between 1-20')
    ], default=1)
    submit = SubmitField('Update Cart')

# class CheckoutForm(FlaskForm):
#     payment_method = SelectField('Payment Method', choices=[
#         ('credit_card', 'Credit Card'),
#         ('debit_card', 'Debit Card'), 
#         ('cash', 'Cash on Delivery')
#     ], validators=[DataRequired()])
#     delivery_notes = TextAreaField('Delivery Instructions', validators=[
#         Optional(),
#         Length(max=200)
#     ])
#     submit = SubmitField('Place Order')

class OrderStatusForm(FlaskForm):
    status = SelectField('Update Status', choices=[
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ], validators=[DataRequired()])
    driver_id = SelectField('Assign Driver', coerce=int, validators=[Optional()])
    submit = SubmitField('Update Status')