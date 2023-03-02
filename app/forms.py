from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField

from wtforms.validators import DataRequired

# FORMS SECTION
class LoginForm(FlaskForm):
    email = EmailField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit_btn = SubmitField('Login')

class PokemonForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    submit_btn = SubmitField('Submit')

class SignUpForm(FlaskForm):
    email = EmailField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit_btn = SubmitField('Sign Up')
