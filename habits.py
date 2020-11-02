from datetime import datetime
from flask import make_response, abort
from config import db
from models import (Habit, HabitSchema)

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

# Create a handler for our read (GET) people
def read():
    """
    This function responds to a request for /api/habits with the complete lists of habits
    
    :return:        sorted list of habits
    """
    # Create the list of people from our data
    habit = Habit.query.order_by(Habit.name).all()    
    
    # Serialize the data for the response
    habit_schema = HabitSchema(many=True)    
    data = habit_schema.dump(habit)    
    return data

def read_one(id):
    """
    This function responds to a request for /api/habits/{name} with one matching habit from habits list
    :param name:   name of the habit to find
    :return:        habit matching name
    """
    
    # Get the habit requested
    habit = Habit.query.filter(Habit.id == id).one_or_none()
    print('Habit = {}'.format(habit))
    if habit is not None:

        # Serialize the data for the response
        habit_schema = HabitSchema()    
        data = habit_schema.dump(habit)    
        return data

    # otherwise, nope, not found
    else:
        abort(
            404, "Habit with id {} not found".format(id)
        )

def create(habit):
    """
    This function creates a new habit in the habits structure based on the passed in habit data
    :param habit:  habit to create in people structure
    :return:        201 on success, 406 on habit exists
    """
    name = habit.get("name", None)
    period = habit.get("period", None)
    goal = habit.get("goal", None)
    
    existing_habit = (
        Habit.query.filter(Habit.name == name)
        .one_or_none()
    )

    # Does the person exist already?
    if existing_habit is None:
        # Create a person instance using the schema and the passed in person
        schema = HabitSchema()
        new_habit = schema.load(habit, session=db.session)

        # Add the person to the database
        db.session.add(new_habit)
        db.session.commit()

        # Serialize and return the newly created person in the response
        data = schema.dump(new_habit)

        return data, 201   

    # Otherwise, they exist, that's an error
    else:
        abort(
            406,
            "Habit with name {name} already exists".format(name=name),
        )
        
    
def update(id, habit):
    """
    This function updates an existing person in the people structure
    :param lname:   last name of person to update in the people structure
    :param person:  person to update
    :return:        updated habit structure
    """
    # Get the habit requested from the db into session
    update_habit = Habit.query.filter(Habit.id == id).one_or_none()

    # Try to find an existing habit with the same name as the update
    name = habit.get("name", None)
    period = habit.get("period", None)
    goal = habit.get("goal", None)    

    existing_habit = (Habit.query.filter(Habit.name == name).one_or_none())
    
    # Are we trying to find a habit that does not exist?
    if update_habit is None:
        abort(
            404,
            "Habit not found for Id: {}".format(id),
        )

    # Would our update create a duplicate of another person already existing?
    elif (existing_habit is not None and existing_habit.id != int(id)):
        abort(
            409,
            "Habit {} exists already".format(name),
        )

    # Otherwise go ahead and update!
    else:
        
        # Create a habit instance using the schema and the passed in habit
        schema = HabitSchema()
        update = schema.load(habit, session=db.session)
        
        
        # Set the id to the habit we want to update
        update.id = update_habit.id

        # Add the person to the database
        db.session.merge(update)
        db.session.commit()

        # Serialize and return the newly created person in the response
        data = schema.dump(update_habit)

        return data, 200


def delete(id):
    """
    This function deletes a habit from the habit table
    :param id:   id of the habit to delete
    :return:        200 on successful delete, 404 if not found
    """
    # Get the habit requested
    habit = Habit.query.filter(Habit.id == id).one_or_none()

    # Did we find a habit?
    if habit is not None:
        db.session.delete(habit)
        db.session.commit()
        return make_response(
            "Habit {} deleted".format(id), 200
        )

    # Otherwise, nope, didn't find that person
    else:
        abort(
            404,
            "Habit not found for Id: {}".format(id),
        )