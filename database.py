from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()  # SQLAlchemy instance

def init_app(app):
    # Link SQLAlchemy with the Flask app
    db.init_app(app)
    Migrate(app, db)
