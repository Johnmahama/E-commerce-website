from wtforms import Form, BooleanField, StringField, PasswordField, validators,IntegerField,TextAreaField,DecimalField
from flask_wtf.file import FileAllowed, FileField,FileRequired


class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35),validators.Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class LoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35),validators.Email()])
    password = PasswordField('New Password', [validators.DataRequired()])
        
class AddproductForm(Form):
    name = StringField('Name',[ validators.DataRequired()])
    price = DecimalField('Price',[validators.DataRequired()])
    discount = IntegerField('Discount',default=0)
    stock = IntegerField('Stock',[validators.DataRequired()])
    description = TextAreaField('Description',[validators.DataRequired()])
    colors = TextAreaField('Colors',[validators.DataRequired()])

    image_1 = FileField('Image_1',validators=[FileAllowed(['jpg','png','gif','jpeg']),'images only please'])
    image_2 = FileField('Image_2',validators=[FileAllowed(['jpg','png','gif','jpeg']),'images only please'])
    image_3 = FileField('Image_3',validators=[FileAllowed(['jpg','png','gif','jpeg']),'images only please'])

    
