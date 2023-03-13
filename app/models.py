from app import db, login
from flask_login import UserMixin # Only use UserMixin for the User Model
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

pokemon_team = db.Table('pokemon_team',
    db.Column('owner_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('catch.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    caught_pokemon = db.relationship('Catch', secondary=pokemon_team, backref='other', lazy='dynamic')
    

    # hashes our password
    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    # checks the hashed password
    def check_hash_password(self, login_password):
        return check_password_hash(self.password, login_password)
    
    # Use this method to register our user attributes
    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])
    
    # Update user attributes
    def update_user(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
    
    # Save the user to database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Update the user to database
    def update_to_db(self):
        db.session.commit()

    def catch_pokemon(self, pokemon):
        self.caught_pokemon.append(pokemon)
        db.session.commit()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class Catch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pokemon_name = db.Column(db.String)
    ability_name= db.Column(db.String)
    base_experience= db.Column(db.Integer)
    front_shiny_url= db.Column(db.String)
    attack_stat= db.Column(db.Integer)
    hp_stat= db.Column(db.Integer)
    defense_stat= db.Column(db.Integer)

    def from_dict(self, data):
        self.pokemon_name = data['pokemon_name']
        self.ability_name= data['ability_name']
        self.base_experience= data['base_experience']
        self.front_shiny_url= data['front_shiny_url']
        self.attack_stat= data['attack_stat']
        self.hp_stat= data['hp_stat']
        self.defense_stat= data['defense_stat']

    # Save the capture to database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    # Update our db
    def update_to_db(self):
        db.session.commit()
    # Delete from db
    def delete_pokemon(self):
        db.session.delete(self)
        db.session.commit()

class Battle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attacker_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    defender_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    attacker = db.relationship('User', foreign_keys=[attacker_id])
    defender = db.relationship('User', foreign_keys=[defender_id])

    
    def from_dict(self, data):
        self.attacker_id = data['attacker_id']
        self.defender_id = data['defender_id']
      
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_to_db(self):
        db.session.commit()
  
    def delete_battle(self):
        db.session.delete(self)
        db.session.commit()

