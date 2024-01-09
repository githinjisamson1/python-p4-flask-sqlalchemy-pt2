#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet, Owner

app = Flask(__name__)
# point to existing db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# set to False to avoid building up too much unhelpful data in memory when our application is running.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# setup for migrations
migrate = Migrate(app, db)

# connect db to app before running
db.init_app(app)


# routes and views
@app.route("/")
def index():
    return make_response('<h1>Welcome to the pet/owner directory!</h1>',
                         200)


# route parameter
@app.route("/pets/<int:id>")
def pet_by_id(id):
    # pet = Pet.query.filter(Pet.id == id).first()
    pet = Pet.query.filter_by(id=id).first()

    if not pet:
        response_body = "<h1>404 pet not found</h1>"
        return make_response(response_body, 404)

    response_body = f'''
        <h1>Information for {pet.name}</h1>
        <h2>Pet Species is {pet.species}</h2>
        <h2>Pet Owner is {pet.owner.name}</h2>
    '''

    return make_response(response_body, 200)


@app.route("/owners/<int:id>")
def owner_by_id(id):
    # owner = Owner.query.filter(Owner.id == id).first()
    owner = Owner.query.filter_by(id=id).first()

    if not owner:
        return make_response("<h1>404 owner not found!</h1>", 404)

    response_body = f'''
    <h1>Information for {owner.name}</h1>
    '''
    # 1:M relationship
    pets = [pet for pet in owner.pets]

    if not pets:
        response_body += f"<h2>Has no pets at this time</h2>"
    else:
        for pet in pets:
            response_body += f"<h2>Has pet {pet.species} named {pet.name}.</h2>"

    return make_response(response_body, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
