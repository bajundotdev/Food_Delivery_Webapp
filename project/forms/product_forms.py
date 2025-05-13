from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FloatField, IntegerField, BooleanField, HiddenField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional, URL
from flask_wtf.file import FileAllowed

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=1000)])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0.01)])
    category = SelectField('Category', validators=[DataRequired()])
    restaurant_id = SelectField('Restaurant', validators=[DataRequired()])
    image = FileField('Product Image', validators=[
        Optional(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    image_url = StringField('Image URL', validators=[Optional(), URL()])
    is_available = BooleanField('Available', default=True)
    submit = SubmitField('Save Product')

class RestaurantProductForm(ProductForm):
    restaurant_id = HiddenField()