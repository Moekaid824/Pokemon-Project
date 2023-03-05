from flask import render_template, request, flash, redirect, url_for
import requests
from app.forms import PokemonForm, LoginForm, RegisterForm
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user

from app import app

# ROUTES SECTION
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data

        # Query from database
        queried_user = User.query.filter_by(email=email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Successfully logged in! Welcome back, {queried_user.first_name}!', 'Success')
            return redirect(url_for('home'))
        else:
            error = 'Invalid email or password'
            flash(f'{error}', 'danger')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)
        
@app.route('/logout', methods=['GET'])
def logout():
    if current_user:
        logout_user()
        flash('You have successfully logged out!', 'Success')
        return redirect(url_for('home'))                   

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():

        new_user_data = {
            'first_name': form.first_name.data.title(),
            'last_name': form.last_name.data.title(),
            'email':  form.email.data.lower(),
            'password':  form.password.data,
        }
        # Create instance of User
        new_user = User()

        # Implementing values from our form data for our instance
        new_user.from_dict(new_user_data)

        # Save our instance to the database
        new_user.save_to_db()
        flash('You have successfully registered!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

    


@app.route("/pokemon", methods=['GET','POST'])
def pokemon():
    form = PokemonForm()
    print(request.method)
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        print(name)
        url = f'https://pokeapi.co/api/v2/pokemon/{name}'
        response = requests.get(url)
        if response.ok:
            pokemon_attributes = response.json()
            pokemon_info={
                    'pokemon_name':pokemon_attributes['name'],
                    'ability_name':pokemon_attributes['abilities'][0]['ability']['name'],
                    'base_experience':pokemon_attributes['base_experience'],
                    'front_shiny_url':pokemon_attributes['sprites']['front_shiny'],
                    'attack_stat':pokemon_attributes['stats'][0]['base_stat'],
                    'hp_stat':pokemon_attributes['stats'][0]['base_stat'],
                    'defense_stat':pokemon_attributes['stats'][0]['base_stat'],
                    }
            print(pokemon_info)
            return render_template('pokemon.html', pokemon_info = pokemon_info, form=form)
        else:
            "This is an invalid option."
            return render_template('pokemon.html', form=form)
    return render_template('pokemon.html', form=form)


