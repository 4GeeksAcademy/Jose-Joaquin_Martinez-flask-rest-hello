from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)
    favorites = relationship('Favorite', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class People(db.Model):
    __tablename__= "people"
    people_id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(50), nullable=False, unique=True)
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    hair_color = db.Column(db.String(15))
    skin_color = db.Column(db.String(15))
    eye_color = db.Column(db.String(15))
    birth_year = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    homeworld = db.Column(db.String(30))
    favorites = relationship('Favorite', backref='character', lazy=True)

    def __repr__(self):
        return '<People %r>' % self.people_id

    def serialize(self):
        return {
            "id": self.people_id,
            "character_name": self.character_name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld
        }

class Planet(db.Model):
    __tablename__= "planets"
    planet_id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String(50), unique=True, nullable=False)
    diameter = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    gravity = db.Column(db.String(10))
    population = db.Column(db.Integer)
    climate = db.Column(db.String(50))
    terrain = db.Column(db.String(50))
    surface_water = db.Column(db.Integer)
    favorites = relationship('Favorite', backref='planet', lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.planet_id

    def serialize(self):
        return {
            "id": self.planet_id,
            "planet_name": self.planet_name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water
        }

class Vehicle(db.Model):
    __tablename__= "vehicles"
    vehicle_id = db.Column(db.Integer, primary_key=True)
    vehicle_name = db.Column(db.String(80), unique=True, nullable=False)
    cargo_capacity = db.Column(db.Integer)
    cost_in_credits = db.Column(db.Integer)
    created = db.Column(db.String(80))
    crew = db.Column(db.Integer)
    length = db.Column(db.Integer)
    manufacturer = db.Column(db.String(80))
    model = db.Column(db.String(80))
    passengers = db.Column(db.Integer)
    vehicle_class = db.Column(db.String(50))
    favorites = relationship('Favorite', backref='vehicle', lazy=True)

    def __repr__(self):
        return '<Vehicle %r>' % self.vehicle_id

    def serialize(self):
        return {
            "id": self.vehicle_id,
            "vehicle_name": self.vehicle_name,
            "cargo_capacity": self.cargo_capacity,
            "cost_in_credits": self.cost_in_credits,
            "created": self.created,
            "crew": self.crew,
            "length": self.length,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "passengers": self.passengers,
            "vehicle_class": self.vehicle_class
        }

class Favorite(db.Model):
    __tablename__= "favorites"
    favorite_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    character_id = db.Column(db.Integer, db.ForeignKey(People.people_id))
    planet_id = db.Column(db.Integer, db.ForeignKey(Planet.planet_id))
    vehicle_id = db.Column(db.Integer, db.ForeignKey(Vehicle.vehicle_id))
    favorite_type = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<Favorite %r>' % self.favorite_id

    def serialize(self):
        serialized_favorite = {
            "id": self.favorite_id,
            "user_id": self.user_id,
            "favorite_type": self.favorite_type
        }

        if self.character_id:
            character = People.query.get(self.character_id)
            serialized_favorite["character_name"] = character.character_name

        if self.planet_id:
            planet = Planet.query.get(self.planet_id)
            serialized_favorite["planet_name"] = planet.planet_name

        if self.vehicle_id:
            vehicle = Vehicle.query.get(self.vehicle_id)
            serialized_favorite["vehicle_name"] = vehicle.vehicle_name

        return serialized_favorite
    