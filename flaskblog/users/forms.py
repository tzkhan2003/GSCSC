from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User
from wtforms.fields.html5 import DateField






class Memberform(FlaskForm):
    token = StringField('Token id/ Trx id',
                           validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    
    birth_date = DateField('Date of Birth',validators=[DataRequired()],format = '%Y-%m-%d' )

    father_name = StringField("Father's Name",
                           validators=[DataRequired(), Length(min=2, max=20)])
    father_ocu = StringField("Father's Occupation",
                           validators=[DataRequired(), Length(min=2, max=20)])
    mother_name = StringField("Mother's Name",
                           validators=[DataRequired(), Length(min=2, max=20)])
    mother_ocu = StringField("Mother's Occupation",
                           validators=[DataRequired(), Length(min=2, max=20)])

    parents_no = StringField("Parents No (Father/Mother",
                           validators=[DataRequired(), Length(min=2, max=20)])
    present_address = StringField("Present Address",
                           validators=[DataRequired(), Length(min=2, max=20)])
    permanent_address = StringField("Permanent Address",
                           validators=[DataRequired(), Length(min=2, max=20)])
    roll = StringField("College Roll",
                           validators=[DataRequired(), Length(min=2, max=20)])

    year = StringField("Academic year",
                           validators=[DataRequired(), Length(min=2, max=20)])

    nid = StringField("NID/Birth Certificate no",
                           validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField("Contact number",
                           validators=[DataRequired(), Length(min=2, max=20)])
    facebook = StringField('Facebook id',
                        validators=[DataRequired(), Length(min=2, max=20)])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])


    exp = StringField("Previous experience with clunning (if any)",
                           validators=[DataRequired(), Length(min=2, max=20)])

    school = StringField("School name (as per SSC)",
                           validators=[DataRequired(), Length(min=2, max=20)])


    submit = SubmitField('Submit')











class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    birth_date = DateField('Date of Birth',validators=[DataRequired()],format = '%Y-%m-%d' )
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
