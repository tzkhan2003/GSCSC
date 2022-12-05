from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed,FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField,IntegerField,FloatField,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User
from wtforms.fields.html5 import DateField
from flaskblog import db
from flaskblog.models import SellerId, User

class Contact(FlaskForm):
    name = StringField('Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])

    message = TextAreaField('Message', validators=[DataRequired()])
    
    submit = SubmitField('Send Message')

class Sellerform(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    birth_date = DateField('Date of Birth',validators=[DataRequired()],format = '%Y-%m-%d' )
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    Parents_No = StringField("Parents No",
                           validators=[DataRequired(), Length(min=2, max=20)])
    address = StringField("Address",
                           validators=[DataRequired(), Length(min=2, max=20)])
    nid = StringField("NID/info no",
                           validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField("Contact number",
                           validators=[DataRequired(), Length(min=2, max=20)])
    panel = StringField("Your post",
                           validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')







'''class Addproducts(FlaskForm):

    name = StringField('Book Name', validators=[DataRequired(), Length(min=2, max=20)])
    page = FloatField('Page No', validators=[DataRequired()])
    link = IntegerField('Link', validators=[DataRequired()])
    stock = IntegerField('Availavality', validators=[DataRequired()])
    #colors = StringField('Colors', validators=[DataRequired()])
    discription = TextAreaField('Discription', validators=[DataRequired()])
    #brand=SelectField('Brand', choices=[('0', 'Select Catagory'), ('py', 'Python'), ('text', 'Plain Text')])
    #catagory=SelectField('Catagory', choices=[('0', 'Select Catagory'), ('py', 'Python'), ('text', 'Plain Text')])

    image_1 = FileField('Image 1', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    image_2 = FileField('Image 2', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    image_3 = FileField('Image 3', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    submit = SubmitField('Add Book')

class Upproducts(FlaskForm):
    name = StringField('Book Name', validators=[DataRequired(), Length(min=2, max=20)])
    page = FloatField('Page No', validators=[DataRequired()])
    link = IntegerField('link', validators=[DataRequired()])
    stock = IntegerField('Availavality', validators=[DataRequired()])
    #colors = StringField('Colors', validators=[DataRequired()])
    discription = TextAreaField('Discription', validators=[DataRequired()])
    #brand=SelectField('Brand', choices=[('0', 'Select Brand'), ('py', 'Python'), ('text', 'Plain Text')])
    #catagory=SelectField('Catagory', choices=[('0', 'Select Catagory'), ('py', 'Python'), ('text', 'Plain Text')])

    image_1 = FileField('Image 1', validators=[FileAllowed(['jpg','png','gif','jpeg'])])
    image_2 = FileField('Image 2', validators=[FileAllowed(['jpg','png','gif','jpeg'])])
    image_3 = FileField('Image 3', validators=[FileAllowed(['jpg','png','gif','jpeg'])])
    submit = SubmitField('Update Book')'''