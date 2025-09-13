#external imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@db.egdumlkkfxknccmvgzxo.supabase.co:5432/postgres"
    db.init_app(app)

    #internal imports (no circular imports)
    from users.routes import users
    from recipe_posts.routes import recipe_posts
    app.register_blueprint(users)
    app.register_blueprint(recipe_posts)
    
    return app
