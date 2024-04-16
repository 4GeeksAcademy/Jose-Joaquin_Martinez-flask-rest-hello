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