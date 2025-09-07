from flask import Blueprint, request, jsonify
from supabase import create_client
from ..forms import CreateRecipeForm
from ..models import db, Post
from utils import current_time

recipe_posts = Blueprint("recipe_posts", __name__)

""" Creating a Supabase client instance"""
SUPABASE_URL = 'https://egdumlkkfxknccmvgzxo.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVnZHVtbGtrZnhrbmNjbXZnenhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc5Njk2MDEsImV4cCI6MjA2MzU0NTYwMX0.9yT_wv-72Hlea4E0Rlo4p8V_aWObnvxksx1UOTdIQlc'
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
""" ************ Recipe Post views ************ """


@recipe_posts.route("/post", methods=["GET", "POST"])
def post():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    user_response = supabase.auth.get_user(token)
    user = user_response.user
    if not user:
        return jsonify({"error": "User not found"}), 404  
    
    data = request.get_json()
    form = CreateRecipeForm(data=data)
    if form.validate():
        #Create Post model and update the necessary databases with new post, not finished
        new_post = Post(
            user_id=user.id,
            title=form.title.data,
            recipe=form.recipe.data,
            image_uri=form.image.data,
            post_comments=[],
            timestamp=current_time(),
            post_likes_count=0
        )
    else:
        return jsonify({"errors": form.errors}), 400

@recipe_posts.route("/search", methods=["GET", "POST"])
def search():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    user_response = supabase.auth.get_user(token)
    user = user_response.user
    if not user:
        return jsonify({"error": "User not found"}), 404 
    #Implement search logic here

@recipe_posts.route("/home", methods=["GET", "POST"])
def home():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    user_response = supabase.auth.get_user(token)
    user = user_response.user
    if not user:
        return jsonify({"error": "User not found"}), 404 
    #Decide what to put on the home page
    