from flask import Blueprint, request, jsonify
from supabase import create_client
from ..forms import CreateRecipeForm, UpdateUserNameForm, UpdateProfilePicForm, UpdateBioForm
from ..models import Profile
from . import db

users = Blueprint("users", __name__)

""" Creating a Supabase client instance"""
SUPABASE_URL = 'https://egdumlkkfxknccmvgzxo.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVnZHVtbGtrZnhrbmNjbXZnenhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc5Njk2MDEsImV4cCI6MjA2MzU0NTYwMX0.9yT_wv-72Hlea4E0Rlo4p8V_aWObnvxksx1UOTdIQlc'
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

""" ************ User Management views ************ """


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
        Profile.query.get(user_id = user.id).update({"username": data.get("username")})
        Profile.query.get(user_id = user.id).update({"bio": data.get("bio")})
        Profile.query.get(user_id = user.id).update({"profile_picture_uri": data.get("profile_picture_uri")})
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
    liked_posts = Profile.query.get(user_id = user.id).liked_posts
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
    commented_posts = Profile.query.get(user_id = user.id).commented_posts
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
    #Implement language selection, dark/light theme, in the future