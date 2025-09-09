from flask import Blueprint, request, jsonify
from supabase import create_client
from ..forms import CreateRecipeForm
from ..models import db, Post, Notification, Profile
from utils import current_time

recipe_posts = Blueprint("recipe_posts", __name__)

# Creating a Supabase client instance
SUPABASE_URL = 'https://egdumlkkfxknccmvgzxo.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVnZHVtbGtrZnhrbmNjbXZnenhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc5Njk2MDEsImV4cCI6MjA2MzU0NTYwMX0.9yT_wv-72Hlea4E0Rlo4p8V_aWObnvxksx1UOTdIQlc'
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

""" ************ Recipe Post views ************ """

@recipe_posts.route("/post", methods=["GET", "POST"])
def post():
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 400
    profile = get_or_create_profile(user)
    if request.data:
        data = request.get_json()
        recipe_form = CreateRecipeForm({"title": data.get("title"), "recipe": data.get("recipe"), "image": data.get("image"), "tags": data.get("tags")})
        if not recipe_form.validate():
            return jsonify({"success": False, "error": recipe_form.errors}), 400
        post = Post(author = Profile, title = data.get("title"), recipe = data.get("recipe"), image_uri = data.get("image"), tags = data.get("tags"), timestamp = current_time(), likes_count = 0)
        db.session.add(post)
        db.session.commit()
        for follower in profile.followers:
            notif = Notification(notified_id = profile.id, post_id = post.id, type = "new_post", message = f"{profile.username} has created a new post!", timestamp = current_time())
            db.session.add(notif)
            db.session.commit()
    

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

""" ************ Helper functions ************ """

def get_user(auth_header):
    token = auth_header.replace("Bearer ", "")
    user_response = supabase.auth.get_user(token)
    user = user_response.user
    return user

def get_or_create_profile(user):
    profile = Profile.query.filter_by(user_id=user.id).first()
    if not profile:
        profile = Profile(
            user_id=user.id,
            bio=f"Hi, I'm {user.email}.",
            username=user.email,
            profile_picture_uri="https://i.pinimg.com/474x/9e/83/75/9e837528f01cf3f42119c5aeeed1b336.jpg?nii=t",
            account_created=current_time(),
            light_mode=True,
            language="English"
        )
        db.session.add(profile)
        db.session.commit()
    return profile