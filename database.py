from flask_sqlalchemy import SQLAlchemy

db.SQLALchemy()

def init_app(app):
    db.init_app(app)

def create_tables():
    db.create_all()