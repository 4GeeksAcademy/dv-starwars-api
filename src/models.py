from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()




class User(db.Model):
    id = db.Column(db.Integer(),  primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }


class People(db.Model):
    id = db.Column(db.Integer(),  primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(80), nullable=False)

    favorite = db.relationship("Favorite", back_populates="people")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender
        }


class Planet(db.Model):
    id = db.Column(db.Integer(),  primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    population = db.Column(db.String(80), nullable=False)

    favorite = db.relationship("Favorite", back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population
        }
    

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    people_id = db.Column(db.Integer(), db.ForeignKey("people.id"), nullable=True)
    planet_id = db.Column(db.Integer(), db.ForeignKey("planet.id"), nullable=True)

    planet = db.relationship("Planet", back_populates="favorite" )
    people = db.relationship("People", back_populates="favorite" )


    def serialize(self):
        return{
            "id": self.id,
            "people": self.planet.serialize(),
            # "planet": self.planet
        }


    
    

