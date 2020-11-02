from datetime import datetime
from config import db, ma
from marshmallow_sqlalchemy import ModelSchema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field


class Habit(db.Model):
    __tablename__ = "habit"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    period = db.Column(db.String(32))
    goal = db.Column(db.Integer)
    creation_date = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class HabitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Habit
        include_relationships = True
        load_instance = True