# server/models.py
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint
from . import db # Import the db instance from server/__init__.py

# --- Models ---

class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    # Relationship: Camper has many Signups
    signups = db.relationship('Signup', backref='camper', lazy=True, cascade='all, delete-orphan')

    # Serializer rules to exclude signups from the default /campers route
    # and prevent recursion when signups nests camper
    serialize_rules = ('-signups.camper',)

    # Validation: name is required and age is between 8 and 18
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise AssertionError('Name is required')
        return name

    @validates('age')
    def validate_age(self, key, age):
        if not (8 <= age <= 18):
            raise AssertionError('Age must be between 8 and 18, inclusive')
        return age

    def __repr__(self):
        return f'<Camper {self.id}: {self.name}, Age: {self.age}>'

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    # Relationship: Activity has many Signups (CASCADE DELETE)
    # Deleting an Activity must remove its associated Signups
    signups = db.relationship('Signup', backref='activity', lazy=True, cascade='all, delete-orphan')

    # Serializer rules to prevent recursion when signups nests activity
    serialize_rules = ('-signups.activity',)

    def __repr__(self):
        return f'<Activity {self.id}: {self.name}, Difficulty: {self.difficulty}>'

class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, nullable=False)  # Hour of the day

    # Foreign Keys
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)

    # Validation: time must be an integer between 0 and 23
    @validates('time')
    def validate_time(self, key, time):
        if not (0 <= time <= 23):
            raise AssertionError('Time must be an integer between 0 and 23 (hour of the day)')
        return time

    # Serializer rules for nested display (POST /signups success case)
    # Nest Camper and Activity details
    serialize_rules = ('-camper.signups', '-activity.signups')

    def __repr__(self):
        return f'<Signup {self.id}: Camper {self.camper_id} for Activity {self.activity_id} at {self.time}:00>'

# Optional: Add database-level constraint for age and time (Good practice, but ORM validation handles the requirement)
# Camper.__table_args__ = (
#     CheckConstraint('age >= 8 AND age <= 18', name='age_range_check'),
# )
# Signup.__table_args__ = (
#     CheckConstraint('time >= 0 AND time <= 23', name='time_range_check'),
# )