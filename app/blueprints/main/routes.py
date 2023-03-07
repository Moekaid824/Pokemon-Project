from flask import render_template, request
import requests
from . import main 
from flask_login import login_required
from app.blueprints.auth.forms import PokemonForm

# ROUTES SECTION
@main.route('/', methods=['GET'])
@login_required
def home():
    return render_template('home.html')

@main.route("/pokemon", methods=['GET','POST'])
@login_required
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
