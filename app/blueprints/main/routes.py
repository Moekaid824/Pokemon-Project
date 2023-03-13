from flask import render_template, request, redirect, url_for, flash
import requests
from . import main 
from flask_login import login_required, current_user
from app.blueprints.auth.forms import PokemonForm, BattleForm, TeamForm
from ...models import User, Catch, Battle

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
            flash('This is an invalid option', 'danger')
            return redirect(url_for('main.pokemon'))
    return render_template('pokemon.html', form=form)

@main.route("/caught_pokemon/<pokename>")
@login_required
def caught_pokemon(pokename):
    caught_pokemon = Catch.query.filter_by(pokemon_name=pokename).first()
    if caught_pokemon:
        current_user.catch_pokemon(caught_pokemon)
        flash(f'Caught {pokename}', 'success')
        return redirect(url_for('main.pokemon'))
    else:
        name = pokename
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
            pokemon=Catch()
            pokemon.from_dict(pokemon_info)
            pokemon.save_to_db()
            current_user.catch_pokemon(pokemon)
            flash(f'You have captured {pokename}!', 'success')
            return redirect(url_for('main.pokemon'))
    return redirect(url_for('main.pokemon'))


@main.route("/team", methods=['GET','POST'])
@login_required
def team():
    team = current_user.caught_pokemon
    form = TeamForm()

    
    if form.validate_on_submit():
        
        if len(team) >= 5:
            flash('You already have the maximum number of Pokemon!', 'danger')
        else:
            name = form.name.data.lower()
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
                pokemon= Catch()
                pokemon.from_dict(pokemon_info)
                pokemon.save_to_db()
                current_user.catch_pokemon(pokemon)
                flash(f'You have added {name} to your team!', 'success')
                return redirect(url_for('main.team'))
            else:
                flash('This is an invalid option', 'danger')


    if request.method == 'POST' and 'remove_pokemon' in request.form:
        pokemon_id = int(request.form['remove_pokemon'])
        pokemon = Catch.query.filter_by(id=pokemon_id).first()
        if pokemon in team:
            current_user.release_pokemon(pokemon)
            flash(f'You have released {pokemon.pokemon_name} from your team!', 'success')
        else:
            flash(f'{pokemon.pokemon_name} is not in your team!', 'danger')
        return redirect(url_for('main.team'))

    return render_template('pokemon_teams.html', team=team, form=form)

@main.route('/battle', methods=['GET', 'POST'])
@login_required
def battle():
    form = BattleForm()
    attacker = None
    defender = None
    if request.method == 'POST' and form.validate_on_submit():
        attacker_id = form.attacker_id.data
        defender_id = form.defender_id.data
        battle = Battle(attacker_id=attacker_id, defender_id=defender_id)
       
        flash('Attack successful!', 'success')
        return redirect(url_for('main.battle'))
    return render_template('battle.html', form=form, attacker=attacker, defender=defender)

