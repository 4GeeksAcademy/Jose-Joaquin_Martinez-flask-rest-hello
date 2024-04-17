import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Vehicle, Favorite
import logging

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET']) 
def get_users():
    users = User.query.all()
    users = list(map(lambda x: x.serialize(), users))
    return jsonify(users), 200

# //TODO People endpoints

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    if not people:
        raise APIException('Character does not exist', 404)
    people = list(map(lambda x: x.serialize(), people))
    return jsonify(people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_by_id(people_id):
    person = People.query.get_or_404(people_id)
    if not person:
        raise APIException('Character does not exist', 404)
    person = person.serialize()
    return jsonify(person), 200

@app.route('/people', methods=['POST'])
def add_people_to_the_table():
    new_character_data = request.json
    existing_character = People.query.filter_by(character_name=new_character_data["character_name"]).first()
    if existing_character:
        return jsonify({'message': 'Character already exists'}), 400

    new_character = People(
        character_name=new_character_data["character_name"],
        height=new_character_data["height"],
        mass=new_character_data["mass"],
        hair_color=new_character_data["hair_color"],
        skin_color=new_character_data["skin_color"],
        eye_color=new_character_data["eye_color"],
        birth_year=new_character_data["birth_year"],
        gender=new_character_data["gender"],
        homeworld=new_character_data["homeworld"]
    )
    db.session.add(new_character)
    db.session.commit()

    serialized_character = new_character.serialize()
    return jsonify(serialized_character), 201


@app.route('/people/<int:people_id>', methods=['PUT'])
def modify_people_to_the_table(people_id):
    character = People.query.get_or_404(people_id)
    if not character:
        raise APIException('Character does not exist', 404)

    data = request.json

    character.character_name = data.get("character_name", character.character_name)
    character.height = data.get("height", character.height)
    character.mass = data.get("mass", character.mass)
    character.hair_color = data.get("hair_color", character.hair_color)
    character.skin_color = data.get("skin_color", character.skin_color)
    character.eye_color = data.get("eye_color", character.eye_color)
    character.birth_year = data.get("birth_year", character.birth_year)
    character.gender = data.get("gender", character.gender)
    character.homeworld = data.get("homeworld", character.homeworld)

    db.session.commit()

    serialized_character = character.serialize()
    return jsonify(serialized_character), 200


@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_people_to_the_table(people_id):
    character = People.query.get_or_404(people_id)
    if not character:
        raise APIException('Character does not exist', 404)

    db.session.delete(character)
    db.session.commit()

    return jsonify('Character deleted'), 200


# //TODO Planets endpoints


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    planets = list(map(lambda x: x.serialize(), planets))
    return jsonify(planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    if not planet:
        raise APIException('Planet does not exist', 404)
    planet = planet.serialize()
    return jsonify(planet), 200


@app.route('/planets', methods=['POST'])
def add_planet_to_the_table():
    new_planet_data = request.json
    existing_planet = Planet.query.filter_by(planet_name=new_planet_data["planet_name"]).first()
    if existing_planet:
        return jsonify({'message': 'Planet already exists'}), 400

    new_planet = Planet(
        planet_name=new_planet_data["planet_name"],
        diameter=new_planet_data["diameter"],
        rotation_period=new_planet_data["rotation_period"],
        orbital_period=new_planet_data["orbital_period"],
        gravity=new_planet_data["gravity"],
        population=new_planet_data["population"],
        climate=new_planet_data["climate"],
        terrain=new_planet_data["terrain"],
        surface_water=new_planet_data["surface_water"]
    )
    db.session.add(new_planet)
    db.session.commit()

    serialized_planet = new_planet.serialize()
    return jsonify(serialized_planet), 201

@app.route('/planets/<int:planet_id>', methods=['PUT'])
def modify_planet_to_the_table(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    if not planet:
        raise APIException('Planet does not exist', 404)

    data = request.json

    planet.planet_name = data.get("planet_name", planet.planet_name)
    planet.diameter = data.get("diameter", planet.diameter)
    planet.rotation_period = data.get("rotation_period", planet.rotation_period)
    planet.orbital_period = data.get("orbital_period", planet.orbital_period)
    planet.gravity = data.get("gravity", planet.gravity)
    planet.population = data.get("population", planet.population)
    planet.climate = data.get("climate", planet.climate)
    planet.terrain = data.get("terrain", planet.terrain)
    planet.surface_water = data.get("surface_water", planet.surface_water)

    db.session.commit()

    serialized_planet = planet.serialize()
    return jsonify(serialized_planet), 200

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet_to_the_table(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    if not planet:
        raise APIException('Planet does not exist', 404)

    db.session.delete(planet)
    db.session.commit()

    return jsonify('Planet deleted'), 200

#  //TODO Vehicles endpoints

@app.route('/vehicles',methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    vehicles = list(map(lambda x: x.serialize(), vehicles))
    return jsonify(vehicles), 200

@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle_by_id(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    if not vehicle:
        raise APIException('Vehicle does not exist', 404)
    vehicle = vehicle.serialize()
    return jsonify(vehicle), 200


@app.route('/vehicles', methods=['POST'])
def add_vehicle_to_the_table():
    new_vehicle_data = request.json
    existing_vehicle = Vehicle.query.filter_by(vehicle_name=new_vehicle_data["vehicle_name"]).first()
    if existing_vehicle:
        return jsonify({'message': 'Vehicle already exists'}), 400

    new_vehicle = Vehicle(
        vehicle_name=new_vehicle_data["vehicle_name"],
        cargo_capacity=new_vehicle_data["cargo_capacity"],
        cost_in_credits=new_vehicle_data["cost_in_credits"],
        created=new_vehicle_data["created"],
        crew=new_vehicle_data["crew"],
        length=new_vehicle_data["length"],
        manufacturer=new_vehicle_data["manufacturer"],
        model=new_vehicle_data["model"],
        passengers=new_vehicle_data["passengers"],
        vehicle_class=new_vehicle_data["vehicle_class"]
    )
    db.session.add(new_vehicle)
    db.session.commit()

    serialized_vehicle = new_vehicle.serialize()
    return jsonify(serialized_vehicle), 201


@app.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def modify_vehicle_to_the_table(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    if not vehicle:
        raise APIException('Vehicle does not exist', 404)

    data = request.json

    vehicle.vehicle_name = data.get("vehicle_name", vehicle.vehicle_name)
    vehicle.cargo_capacity = data.get("cargo_capacity", vehicle.cargo_capacity)
    vehicle.cost_in_credits = data.get("cost_in_credits", vehicle.cost_in_credits)
    vehicle.created = data.get("created", vehicle.created)
    vehicle.crew = data.get("crew", vehicle.crew)
    vehicle.length = data.get("length", vehicle.length)
    vehicle.manufacturer = data.get("manufacturer", vehicle.manufacturer)
    vehicle.model = data.get("model", vehicle.model)
    vehicle.passengers = data.get("passengers", vehicle.passengers)
    vehicle.vehicle_class = data.get("vehicle_class", vehicle.vehicle_class)

    db.session.commit()

    serialized_vehicle = vehicle.serialize()
    return jsonify(serialized_vehicle), 200

@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle_to_the_table(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    if not vehicle:
        raise APIException('Vehicle does not exist', 404)

    db.session.delete(vehicle)
    db.session.commit()

    return jsonify('Vehicle deleted'), 200


# //TODO Favorite endpoints


@app.route('/favorites/<int:user_id1>', methods=['GET']) 
def get_favorites_by_user_id(user_id1):
    favorites = Favorite.query.filter_by(user_id=user_id1).all()
    if not favorites:
        return jsonify([])
    favorites = list(map(lambda x: x.serialize(), favorites))
    return jsonify(favorites), 200

@app.route('/favorites', methods=['POST'])
def add_favourite_by_id():
    favorite_data = request.json
    new_favorite = Favorite(
        user_id=favorite_data["user_id"],
        character_id=favorite_data.get("character_id"),
        planet_id=favorite_data.get("planet_id"),
        vehicle_id=favorite_data.get("vehicle_id"),
        favorite_type=favorite_data["favorite_type"],
    )
    db.session.add(new_favorite)
    db.session.commit()

    serialized_favorite = new_favorite.serialize()
    return jsonify(serialized_favorite), 201

@app.route('/favorite/<int:id>', methods=['DELETE'])
def delete_from_favorites(id):
    favorite = Favorite.query.get_or_404(id)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify('Deleted element'), 200




if __name__ == "__main__":
    app.run(debug=True)