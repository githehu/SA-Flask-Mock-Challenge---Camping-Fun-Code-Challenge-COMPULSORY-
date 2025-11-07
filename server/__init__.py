# server/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Instantiate Extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=None):
    app = Flask(__name__)

    # --- Configuration ---
    # Use SQLite for simplicity, database.db will be in the 'instance' folder
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_APP'] = os.environ.get('FLASK_APP', 'server.app')

    # --- Initialize Extensions ---
    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register routes here to avoid circular imports in a large app,
    # but for simplicity, we'll import everything in app.py for this small project.

    return app

# Import models to make them known to Flask-Migrate
from . import models 

# Import db and app setup helpers for easy use in app.py and routes.py