from flask import Blueprint, request, jsonify
from supabase import create_client
from ..forms import CreateRecipeForm
from ..models import db, Post, Notification, Profile
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
        return jsonify({"success": False, "error": "User not found"}), 400 
    data = request.get_json()
    recipe_form = CreateRecipeForm({"title": data.get("title"), "recipe": data.get("recipe"), "image": data.get("image"), "tags": data.get("tags")})
    if not recipe_form.validate():
        return jsonify({"success": False, "error": recipe_form.errors}), 400
    
    profile = Profile.query.filter_by(user_id = user.id)

    post = Post()
    post.author = profile
    post.title = data.get("title")
    post.recipe = data.get("recipe")
    post.image_uri = data.get("image")
    post.tags = data.get("tags")
    post.comments = []
    post.timestamp = current_time()
    post.likes_count = 0
    db.session.add(post)
    db.session.commit()

    for follower in profile.followers:
        notif = Notification()
        notif.user_id = follower.id
        notif.post_id = post.id
        notif.type = "new_post"
        notif.message = f"{profile.username} has created a new post!"
        notif.timestamp = current_time()
        notif.read = False
        db.session.add(notif)
        db.session.commit()
    return jsonify({"success": False}), 200

@recipe_posts.route("/search", methods=["GET", "POST"])
def search():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    user_response = supabase.auth.get_user(token)
    user = user_response.user
    if not user:
        return jsonify({"error": "User not found"}), 400
    #Implement search logic here

@recipe_posts.route("/home", methods=["GET", "POST"])
def home():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    user_response = supabase.auth.get_user(token)
    user = user_response.user
    if not user:
        return jsonify({"error": "User not found"}), 400 
    #Decide what to put on the home page
    