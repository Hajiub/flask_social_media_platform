from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, HiddenField, EmailField, DateField, BooleanField, TextAreaField
from .models import User
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, Optional
from sqlalchemy import func
from flask_wtf.file import FileField, FileAllowed, FileSize

class SigninForm(FlaskForm):
    def validate_email(self, email):
        user = User.query.filter(func.lower(User.email) == func.lower(email.data)).first()
        if user:
            raise ValidationError("Email already exists!")

    first_name  = StringField('First name:', validators=[Length(min=3, max=30), DataRequired()])
    last_name   = StringField('Last name:', validators=[Length(min=4, max=30), DataRequired()])
    email       = EmailField(label='Email Address:', validators=[Email(), DataRequired()])
    password1   = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2   = PasswordField(label='Confirm Password:', validators=[EqualTo('password1', message='Please Enter the same passwords!'), DataRequired()])
    birthday    = DateField('Birthday:', validators=[DataRequired()])
    submit      = SubmitField(label='Sign In')


class LoginForm(FlaskForm):
    email       = EmailField(label='Email:', validators=[Email(), DataRequired()])
    password    = PasswordField(label='Password:', validators=[DataRequired()])
    remember_me    = BooleanField(label="Remeber Me")
    
    submit      = SubmitField(label='Log in')

class CreatePostForm(FlaskForm):
    
    content = TextAreaField('Create your own post!:', validators=[Length(min=3), DataRequired()])
    image   = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Only JPEG and PNG images are allowed.'), FileSize(max_size=5 * 1024 * 1024, message='File size must be less than 5MB.')])
    create  = SubmitField(label="Create!")

class CreateCommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[Length(min=3), DataRequired()])
    create  = SubmitField(label="Submit")

class UpdatePostForm(FlaskForm):
    
    content = TextAreaField(validators=[Length(min=4)])
    image   = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Only JPEG and PNG images are allowed.'), FileSize(max_size=5 * 1024 * 1024, message='File size must be less than 5MB.')])
    update  = SubmitField(label="Update!")


class FinishProfile(FlaskForm):
    pro_pic  = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Only JPEG and PNG images are allowed.'), FileSize(max_size=5 * 1024 * 1024, message='File size must be less than 5MB.')])
    bio       = TextAreaField(validators=[Optional() ,Length(min=10)])
    add       = SubmitField(label='Add')

