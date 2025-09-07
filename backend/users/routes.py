from flask import Blueprint, request, jsonify
from supabase import create_client
from ..forms import CreateRecipeForm, UpdateUserNameForm, UpdateProfilePicForm, UpdateBioForm
from ..models import Profile
from . import db, current_time

users = Blueprint("users", __name__)

""" Creating a Supabase client instance"""
SUPABASE_URL = 'https://egdumlkkfxknccmvgzxo.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVnZHVtbGtrZnhrbmNjbXZnenhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc5Njk2MDEsImV4cCI6MjA2MzU0NTYwMX0.9yT_wv-72Hlea4E0Rlo4p8V_aWObnvxksx1UOTdIQlc'
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

""" ************ User Management views ************ """

@users.route("/initialize_profile", methods=["POST"])
def create_profile():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    user_response = supabase.auth.get_user(token)
    user = user_response.user
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 400
    if not Profile.query.filter_by(user_id = user.id).first():
        new_profile = Profile()
        new_profile.user_id = user.id
        new_profile.bio = f"Hi, I'm {user.email}."
        new_profile.username = user.email
        new_profile.profile_picture_uri = "https://i.pinimg.com/474x/9e/83/75/9e837528f01cf3f42119c5aeeed1b336.jpg?nii=t"
        new_profile.account_created = current_time()
        new_profile.light_mode = True
        new_profile.language = "English"
        new_profile.followers = []
        new_profile.following = []
        db.session.add(new_profile)
        db.session.commit()
    return jsonify({"success": True}), 200

@users.route("/profile", methods=["GET", "POST"])
def profile():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    user_response = supabase.auth.get_user(token)
    user = user_response.user
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 400
    if request.data:
        data = request.get_json()
        errors = {}
        if data.get("username"):
            username_form = UpdateUserNameForm({"username": data.get("username")})
            if not username_form.validate():
                errors["username"] = username_form.errors
        if data.get("profile_picture_uri"):
            profile_picture_uri_form = UpdateProfilePicForm({"picture": data.get("profile_picture_uri")})
            if not profile_picture_uri_form.validate():
                errors["pfp_pic"] = profile_picture_uri_form.errors
        if data.get("bio"):
            bio_form = UpdateBioForm({"bio": data.get("bio")})
            if not bio_form.validate():
                errors["bio"] = bio_form.errors        
        if errors:
            return jsonify({"success": False, "errors": errors}), 400
        Profile.query.filter_by(user_id = user.id).update({"username": data.get("username")})
        Profile.query.filter_by(user_id = user.id).update({"bio": data.get("bio")})
        Profile.query.filter_by(user_id = user.id).update({"profile_picture_uri": data.get("profile_picture_uri")})
        db.session.commit()
    return jsonify({"success": True}), 200

@users.route("/favorites", methods=["GET"])
def favorites(): 
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    user_response = supabase.auth.get_user(token)
    user = user_response.user
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 400
    liked_posts = Profile.query.filter_by(user_id = user.id).liked_posts
    if not liked_posts:
        return jsonify({"success": True, "empty": True}), 200
    return jsonify({"success": True, "liked_posts": liked_posts}), 200

@users.route("/comments", methods=["GET"])
def comments():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    user_response = supabase.auth.get_user(token)
    user = user_response.user
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 400
    commented_posts = Profile.query.filter_by(user_id = user.id).commented_posts
    if not commented_posts:
        return jsonify({"success": True, "empty": True}), 200
    return jsonify({"success": True, "liked_posts": commented_posts}), 200

@users.route("/settings", methods=["GET", "POST"])
def settings():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    user_response = supabase.auth.get_user(token)
    user = user_response.user
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 400
    if request.data:
        data = request.get_json()
        #Light/Dark Mode and Language Preferences will be buttons, no need for Forms
        if data.get("light_mode"):
            Profile.query.filter_by(user_id = user.id).update({"light_mode": data.get("light_mode")})
        if data.get("language"):    
            Profile.query.filter_by(user_id = user.id).update({"language": data.get("language")})
        db.session.commit()
    return jsonify({"success": True}), 200