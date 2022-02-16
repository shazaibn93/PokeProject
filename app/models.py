from app import db, login
from flask_login import UserMixin #This is just for the user model 
from datetime import datetime as dt 
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

class Caughtem(db.Model):
    pokeid = db.Column(db.Integer, db.ForeignKey('poketeam.id'), primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default = dt.utcnow)
    wins = db.Column(db.Integer, default = 0)
    losses = db.Column(db.Integer, default = 0)
    battles = db.Column(db.Integer, default = 0 )
    squad = db.relationship(
        'Poketeam',
        secondary = 'caughtem',
        backref ='user',
        lazy ='dynamic',
    )

    def total_attack(self):
        total = 0
        for pokemon in self.squad:
            total += int(pokemon.attack)
            return str(total)

    def battle_count(self,user):
        self.battles += 1
        db.session.commit()   

    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'
    
    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def team_full(self):
        return self.squad.count() < 5
    
    def inteam(self, data):
        if self.squad.filter_by(data) != None:
            return True
        else:
            return False
    
    def add_to_team(self, obj):
        if len(list(self.squad)) < 5:
            self.squad.append(obj)
            self.save()
        else:
            pass
    
    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])

    #Save user to database
    def save(self):
        db.session.add(self)
        db.session.commit()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Poketeam (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    hp = db.Column(db.String(50))
    defense = db.Column(db.String(50))
    attack = db.Column(db.String(50))
    ability_1 = db.Column(db.String(50))
    ability_2 = db.Column(db.String(50))
    sprites = db.Column(db.String(500))

    def __repr__(self):
        return f'<Post: {self.id} | {self.name}>'

    def from_dict(self, data):
        self.name = data['name']
        self.hp = data['hp']
        self.defense = data['defense']
        self.attack = data['attack']
        self.ability_1 = data['ability_1']
        self.ability_2 = data['ability_2']
        self.sprites = data['sprite']
    
    def exists(name):
        return Poketeam.query.filter_by(name=name).first()
    
    def save(self):
        db.session.add(self) # add the user to the db session
        db.session.commit() #save everything in the session to the database

