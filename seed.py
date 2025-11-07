# seed.py
from server.app import app
from server.models import db, Camper, Activity, Signup
from random import randint, choice

# Ensure the app context is pushed
with app.app_context():
    print("Clearing database...")
    Signup.query.delete()
    Camper.query.delete()
    Activity.query.delete()
    db.session.commit()

    print("Creating Activities...")
    activities = []
    activity_names = ["Archery", "Swimming", "Hiking", "Campfire Stories", "Canoeing", "Rock Climbing"]
    for i in range(1, 7):
        activity = Activity(
            name=activity_names[i-1], 
            difficulty=randint(1, 5)
        )
        activities.append(activity)
        db.session.add(activity)

    print("Creating Campers...")
    campers = []
    camper_names = ["Caitlin", "Lizzie", "Nicholas", "Ashley", "Zoe", "Mike", "Jenna", "Sam"]
    for i in range(1, 9):
        camper = Camper(
            name=f"{camper_names[i-1]} Doe", 
            age=randint(8, 18)
        )
        campers.append(camper)
        db.session.add(camper)
    
    db.session.commit()

    print("Creating Signups...")
    # Create 20 random signups
    for _ in range(20):
        signup = Signup(
            camper_id=choice(campers).id,
            activity_id=choice(activities).id,
            time=randint(0, 23)
        )
        db.session.add(signup)
    
    db.session.commit()
    print("Seeding complete!")