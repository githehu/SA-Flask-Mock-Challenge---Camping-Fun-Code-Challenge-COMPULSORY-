# SA Flask Mock Challenge — Camping Fun

This is a small Flask REST API used for a mock challenge about a camping application. It provides endpoints for managing Campers, Activities, and Signups. The project contains simple validation rules and uses SQLite by default.

## Tech stack

- Python 3.12 (virtualenv provided in `env/`)
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- SQLite (default, file-based)

## Project layout

- `server/` — application package
	- `__init__.py` — app factory and extension setup
	- `app.py` — creates app instance and registers the API blueprint
	- `models.py` — SQLAlchemy models: `Camper`, `Activity`, `Signup`
	- `routes.py` — API route definitions
- `instance/` — database file will be created here by default (or current working directory)
- `tests/` — pytest tests
- `seed.py` — helper to seed the database

## Getting started

1. Create and activate a virtual environment (or use the included `env/`):

	 python -m venv env
	 source env/bin/activate

2. Install dependencies:

	 pip install -r requirements.txt

3. (Optional) Create a `.env` file to override defaults. Supported env vars:

- `DATABASE_URI` — SQLAlchemy database URI (defaults to `sqlite:///app.db`)
- `FLASK_APP` — the Flask app import path (defaults to `server.app`)

4. Initialize the database and run migrations (Flask-Migrate):

	 export FLASK_APP=server.app
	 flask db init    # only if migrations not yet initialized
	 flask db migrate -m "Initial migration"
	 flask db upgrade

5. Seed the database (if `seed.py` is present and configured):

	 python seed.py

6. Run the app locally:

	 python -m server.app

The server listens on port 5000 by default.

## API Reference

Base URL: http://localhost:5000/

Camper

- GET /campers
	- Returns a list of all campers. Each camper includes `id`, `name`, and `age` (signups excluded).
	- Response: 200

- GET /campers/<id>
	- Returns camper details including nested `signups` and each signup's `activity`.
	- Response: 200 or 404 if not found

- POST /campers
	- Create a new camper. JSON body: { "name": string, "age": integer }
	- Validation: `name` is required; `age` must be between 8 and 18 (inclusive).
	- Success: 201 with the created camper object.
	- Validation errors: 400 with `{ "errors": ["validation errors"] }`

- PATCH /campers/<id>
	- Update a camper's `name` and/or `age`.
	- Same validation rules as POST.
	- Success: 202 with updated camper.
	- 404 if camper not found.

Activity

- GET /activities
	- Returns a list of activities. Each activity includes `id`, `name`, and `difficulty`.
	- Response: 200

- DELETE /activities/<id>
	- Deletes an activity and cascades to remove its signups.
	- Success: 204 (empty body)
	- 404 if activity not found.

Signup

- POST /signups
	- Create a signup linking a camper and an activity. JSON body: { "camper_id": int, "activity_id": int, "time": int }
	- Validation: `time` must be an integer in [0, 23] (hour of the day). Camper and Activity must exist.
	- Success: 201 with the created signup; response nests camper and activity details (signup serializer hides recursive fields).
	- Validation errors: 400 with `{ "errors": ["validation errors"] }`

General errors: 404 handler returns `{ "error": "Resource not found" }`.

## Model validation rules (quick reference)

- Camper:
	- name: required (non-empty)
	- age: 8 <= age <= 18
- Activity: name (string), difficulty (integer)
- Signup:
	- time: 0 <= time <= 23
	- camper_id and activity_id must reference existing records

## Running tests

Run the test suite with pytest:

	 pytest -q

The project includes tests in the `tests/` directory. Running the tests will also show any missing dependencies or configuration issues.

## Notes & tips

- The app uses an application factory pattern (`create_app`) in `server/__init__.py` so it's easy to configure different environments.
- By default the database URI uses `sqlite:///app.db`. Set `DATABASE_URI` in a `.env` file to change this.
- The repository includes a virtual environment under `env/`. You can use it directly or recreate one.

## Contact

If you have questions about the mock challenge or need help running the project, open an issue or contact the maintainer.

---
Generated README for the Flask mock challenge project.