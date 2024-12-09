"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, People, Planet, User, Favorite
#from models import Person

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

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# gel all people
@app.route("/people", methods=["GET"])
def get_all_people():
    try:
        people = People.query.all()
        return jsonify([item.serialize() for item in people]), 200
    except Exception as err:
        return jsonify({"message":f"Error: {err.args}"}), 500


# get one people
@app.route("/people/<int:theid>", methods=["GET"])
def get_one_people(theid=None):
    try:
        people = People.query.get(theid)

        if people is None:
            return jsonify({"message": "user no found"}), 404
        else:
            return jsonify(people.serialize()), 200

    except Exception as err:
        return jsonify({"message" f"Error: {err}"}), 500


# gel all planet
@app.route("/planet", methods=["GET"])
def get_all_planet():
    try:
        people = Planet.query.all()
        return jsonify([item.serialize() for item in people]), 200
    except Exception as err:
        return jsonify({"message":f"Error: {err.args}"}), 500


# get one planet
@app.route("/planet/<int:theid>", methods=["GET"])
def get_one_planet(theid=None):
    try:
        planet = Planet.query.get(theid)

        if planet is None:
            return jsonify({"message": "user no found"}), 404
        else:
            return jsonify(planet.serialize()), 200

    except Exception as err:
        return jsonify({"message" f"Error: {err}"}), 500


@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_planet_fav(planet_id=None):
    
    try:
        body = request.json
        fav = Favorite()
        fav.planet_id = planet_id
        fav.user_id = body["user_id"]

        db.session.add(fav)
        db.session.commit()

        return jsonify("user agregado exitosamente"), 201

    except Exception as err:
        return jsonify({"message":f"Error {err.args}"})
    

@app.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_people_fav(people_id=None):
    
    try:
        body = request.json
        fav = Favorite()
        fav.people_id = people_id
        fav.user_id = body["user_id"]
        fav.planet_id=None

        db.session.add(fav)
        db.session.commit()

        return jsonify("user agregado exitosamente"), 201

    except Exception as err:
        return jsonify({"message":f"Error {err.args}"})
    





# get all users
@app.route("/user", methods=["GET"])
def get_all_user():
    try:
        users = User.query.all()

        return jsonify([item.serialize() for item in users])
    except Exception as err:
        return jsonify({"message":f"Error: {err}"})



@app.route("/users/favorites", methods=["GET"])
def get_all_user_fav():
    try:
        fav = Favorite.query.filter_by(user_id=1).all()
        print(fav[0].serialize())
        return jsonify(list(map(lambda item: item.serialize(), fav))), 200
        return jsonify("trabajando por usted"), 200
    except Exception as err:
        return jsonify(f"error {err.args}")


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
