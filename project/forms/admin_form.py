from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FloatField, IntegerField, BooleanField, HiddenField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional
from flask_wtf.file import FileRequired, FileAllowed

#####################
# Admin Forms       #
#####################

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
    product_id = StringField('Product ID', validators=[DataRequired(), Length(min=2, max=100)])
    product_name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=100)])
    category = SelectField('Category', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0.01)])
    is_active = SelectField('Status', validators=[DataRequired()])
    food_rating = FloatField('Food Rating', default=100)
    prep_time_est = FloatField('Prepping Time Est', validators=[NumberRange(min=1)], default=10)
    restaurant_id = StringField('Restaurant')
    deleted = StringField('Deleted', default=0)
    food_image_url = FileField('Product Image', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Save Product')

class RestaurantForm(FlaskForm):
    name = StringField('Restaurant Name', validators=[DataRequired(), Length(min=2, max=100)])
    address = StringField('Address', validators=[DataRequired(), Length(min=5, max=200)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    website = StringField('Website', validators=[Optional(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=1000)])
    image = FileField('Restaurant Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Save Restaurant')

class CategoryForm(FlaskForm):
    category_id = StringField('Category ID', validators=[DataRequired()])
    category_name = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=100)])