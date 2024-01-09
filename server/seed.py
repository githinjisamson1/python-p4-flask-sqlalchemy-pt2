#!/usr/bin/env python3

from random import choice as rc

from faker import Faker

from app import app
from models import db, Owner, Pet

# db is generated with each new run of the application- it lives in models.py/connect db and application
# db.init_app(app)

fake = Faker()

# ensures that applications fail quickly if they are not configured with this important context.
with app.app_context():
    # empty tables before seeding
    Pet.query.delete()
    Owner.query.delete()

    # track owner objects
    owners = []

    # generate 50 objects
    for item in range(50):
        owner = Owner(name=fake.name())
        owners.append(owner)

    # insert to db
    db.session.add_all(owners)

    # effect changes
    db.session.commit()

    pets = []
    for item in range(100):
        species = ['Dog', 'Cat', 'Chicken', 'Hamster', 'Turtle']
        pet = Pet(name=fake.first_name(), species=rc(
            species), owner=rc(owners))
        pets.append(pet)

    db.session.add_all(pets)
    db.session.commit()


# QUERIES
# Queries in Flask-SQLAlchemy have access to all of the same methods as those in vanilla SQLAlchemy- just remember to start your statements with models!

# // imports
# >> with app.app_context():
# = 'Ben').all()
#  => [<Pet Owner Brenda Hernandez>, <Pet Owner Brian Stone>, ...]

# >> with app.app_context():
# ...     Owner.query.filter(Owner.name <= 'Ben').limit(2).all()
# ...
#  => [<Pet Owner Alan Bryant>, <Pet Owner Allison Phillips DDS>]