#External imports
from flask import Flask, request, jsonify, redirect, url_for, Blueprint
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
#Internal imports
from .users.routes import users
from .recipe_posts.routes import recipe_posts

#TODO

def create_app(test_config=None):
    app = Flask(__name__)

    app.register_blueprint(recipe_posts)
    app.register_blueprint(users)
    #REPLACE THIS
    #connect to the supabase database upon server initialization
    app.config['SQLALCHEMY_DATABASE_URI'] = 'REPLACE THIS'
    db = SQLAlchemy(app)
    db.create_all()

    return app
