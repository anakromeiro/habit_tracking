import os
from config import db
from models import Habit

# Data to initialize database with
# Data to serve with our API
HABITS = [
    {'name':'Reading', 'period': 'Weekly', 'goal':3},
    {'name':'Exercises','period': 'Daily', 'goal':1},
    {'name':'Study','period': 'Daily', 'goal':2}    
]

# Delete database file if it exists currently
if os.path.exists("habits_tracker.db"):
    os.remove("habits_tracker.db")

# Create the database
db.create_all()

# iterate over the PEOPLE structure and populate the database
for habit in HABITS:
    h = Habit(name=habit.get("name"), period=habit.get("period"), goal=habit.get("goal"))
    db.session.add(h)

db.session.commit()