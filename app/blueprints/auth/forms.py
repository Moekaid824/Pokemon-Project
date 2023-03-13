from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, DateField, SubmitField, StringField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, EqualTo
from app.models import User

# FORMS SECTION
class PokemonForm(FlaskForm):
    name = StringField('Pokemon Name:', validators=[DataRequired()])
    submit_btn = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = EmailField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit_btn = SubmitField('Login')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    email = EmailField('Email:', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired(), EqualTo('password')])
    submit_btn = SubmitField('Register')

class EditProfileForm(FlaskForm):
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    email = EmailField('Email:', validators=[DataRequired()])
    submit_btn = SubmitField('Update')

class PokemonCatchForm(FlaskForm):
    name = StringField('Pokemon Name:', validators=[DataRequired()])
    location = StringField('Location:', validators=[DataRequired()])
    date = DateField('Date:', validators=[DataRequired()])
    submit_btn = SubmitField('Catch')

class PokemonTeamForm(FlaskForm):
    name = StringField('Team Name:', validators=[DataRequired()])
    pokemon1 = StringField('Pokemon 1:', validators=[DataRequired()])
    pokemon2 = StringField('Pokemon 2:')
    pokemon3 = StringField('Pokemon 3:')
    pokemon4 = StringField('Pokemon 4:')
    pokemon5 = StringField('Pokemon 5:')
    pokemon6 = StringField('Pokemon 6:')
    submit_btn = SubmitField('Create Team')


class TeamForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    pokemon = SelectMultipleField('Pokemon', coerce=int, validators=[DataRequired()])

class BattleForm(FlaskForm):
    attacker_id = StringField('Attacker ID:', validators=[DataRequired()])
    defender_id = StringField('Defender ID:', validators=[DataRequired()])
    submit_btn = SubmitField('Attack')
