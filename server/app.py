# server/app.py
import os
from . import create_app
from .routes import api_bp # Import the Blueprint
from .models import db, Camper, Activity, Signup # Import models for CLI/migrations

# Create the application instance
app = create_app()

# Register the Blueprint
app.register_blueprint(api_bp)

# If running directly, start the server
if __name__ == '__main__':
    # Set the FLASK_APP environment variable (important for 'flask db' commands)
    os.environ['FLASK_APP'] = 'server.app'
    app.run(port=5000, debug=True)

