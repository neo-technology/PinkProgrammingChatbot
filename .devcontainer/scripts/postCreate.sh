# Create and activate venv using uv
uv venv .venv
source .venv/bin/activate

uv sync
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=0
flask run