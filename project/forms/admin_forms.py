from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FloatField, IntegerField, BooleanField, HiddenField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional
from flask_wtf.file import FileRequired, FileAllowed
from product_forms import ProductForm

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



