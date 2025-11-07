# server/routes.py
from flask import request, jsonify, Blueprint
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import exc as orm_exc
from .models import db, Camper, Activity, Signup

# Use a Blueprint for organizing routes
api_bp = Blueprint('api', __name__, url_prefix='/')

# --- Helper Function for Validation Errors ---
def validation_error_response():
    return jsonify({"errors": ["validation errors"]}), 400

# --- Camper Routes ---

@api_bp.route('/campers', methods=['GET'])
def list_campers():
    """GET /campers: List all campers (exclude signups)."""
    campers = Camper.query.all()
    # Use serialize() with the default rules (which exclude 'signups')
    return jsonify([camper.to_dict() for camper in campers]), 200

@api_bp.route('/campers/<int:id>', methods=['GET'])
def get_camper_by_id(id):
    """GET /campers/<int:id>: Camper details incl. signups (each signup nests activity)."""
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({"error": "Camper not found"}), 404
    
    # Use serialize(rules=()) to include all attributes, including the 'signups' relationship
    return jsonify(camper.to_dict(rules=('signups', 'signups.activity'))), 200

@api_bp.route('/campers', methods=['POST'])
def create_camper():
    """POST /campers: Create a new camper."""
    data = request.get_json()
    try:
        new_camper = Camper(
            name=data.get('name'),
            age=data.get('age')
        )
        db.session.add(new_camper)
        db.session.commit()
        # Success response: Camper object (id, name, age)
        return jsonify(new_camper.to_dict()), 201
    except AssertionError:
        db.session.rollback()
        return validation_error_response()
    except Exception:
        db.session.rollback()
        # Catch other potential errors like missing required fields if not handled by AssertionError
        return validation_error_response()

@api_bp.route('/campers/<int:id>', methods=['PATCH'])
def update_camper(id):
    """PATCH /campers/<int:id>: Update camper name and/or age (exclude signups)."""
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({"error": "Camper not found"}), 404

    data = request.get_json()
    try:
        if 'name' in data:
            camper.name = data['name']
        if 'age' in data:
            camper.age = data['age']
        
        db.session.commit()
        # Success response: Updated camper
        return jsonify(camper.to_dict()), 202
    except AssertionError:
        db.session.rollback()
        return validation_error_response()
    except Exception:
        db.session.rollback()
        return validation_error_response()


# --- Activity Routes ---

@api_bp.route('/activities', methods=['GET'])
def list_activities():
    """GET /activities: List all activities."""
    activities = Activity.query.all()
    return jsonify([activity.to_dict() for activity in activities]), 200

@api_bp.route('/activities/<int:id>', methods=['DELETE'])
def delete_activity(id):
    """DELETE /activities/<int:id>: Delete an activity and its signups (cascade)."""
    activity = Activity.query.get(id)
    if not activity:
        return jsonify({"error": "Activity not found"}), 404
    
    db.session.delete(activity)
    db.session.commit()
    # Success response: Empty body
    return '', 204

# --- Signup Routes ---

@api_bp.route('/signups', methods=['POST'])
def create_signup():
    """POST /signups: Create a signup for an existing camper & activity."""
    data = request.get_json()
    camper_id = data.get('camper_id')
    activity_id = data.get('activity_id')
    time = data.get('time')
    
    # Check if Camper and Activity exist
    if not Camper.query.get(camper_id) or not Activity.query.get(activity_id):
        # Even though the prompt doesn't specify an error for missing foreign key, 
        # a validation error or 404 is appropriate. Sticking to the validation error 
        # response for all errors in the POST logic per spec.
        return validation_error_response()

    try:
        new_signup = Signup(
            camper_id=camper_id,
            activity_id=activity_id,
            time=time
        )
        db.session.add(new_signup)
        db.session.commit()
        
        # Success response: Signup with nested camper & activity
        # Uses the configured serialize_rules on the Signup model
        return jsonify(new_signup.to_dict()), 201
    except AssertionError as e:
        db.session.rollback()
        # The ORM-level validation failed (e.g., time out of range)
        return validation_error_response()
    except IntegrityError:
        db.session.rollback()
        # Catch potential foreign key or other integrity errors (though ORM checks above should catch most)
        return validation_error_response()
    except Exception:
        db.session.rollback()
        return validation_error_response()

# --- Error Handling ---

@api_bp.app_errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404