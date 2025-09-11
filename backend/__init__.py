#external imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#internal imports
from .users.routes import users
from .recipe_posts.routes import recipe_posts

def create_app(test_config=None):
    app = Flask(__name__)
    app.register_blueprint(recipe_posts)
    app.register_blueprint(users)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@db.egdumlkkfxknccmvgzxo.supabase.co:5432/postgres"
    db = SQLAlchemy(app)
    db.create_all()
    return app
