from flask import render_template, request
import requests
from app.forms import PokemonForm, LoginForm, SignUpForm
from app import app

# ROUTES SECTION
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        if email in app.config.get('REGISTERED_USERS') and password == app.config.get('REGISTERED_USERS').get(email).get('password'):
            return f'Sign up Successful! Hello, {app.config.get("REGISTERED_USERS").get(email).get("name")}'
        else:
            return render_template('signup.html', form=form)
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        if email in app.config.get('REGISTERED_USERS') and password == app.config.get('REGISTERED_USERS').get(email).get('password'):
            return f"Login Successful! Welcome {app.config.get('REGISTERED_USERS').get(email).get('name')}"
        else:
            error = 'Incorrect Email/Password'
            return render_template('login.html', error=error, form=form)
    return render_template('login.html', form=form)

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


