from flask import Blueprint, request, jsonify
from supabase import create_client
from ..forms import CreateRecipeForm, UpdateUserNameForm, UpdateProfilePicForm, UpdateBioForm
from ..models import Profile
from . import db, current_time

users = Blueprint("users", __name__)

#Creating a supabase client instance
SUPABASE_URL = 'https://egdumlkkfxknccmvgzxo.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVnZHVtbGtrZnhrbmNjbXZnenhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc5Njk2MDEsImV4cCI6MjA2MzU0NTYwMX0.9yT_wv-72Hlea4E0Rlo4p8V_aWObnvxksx1UOTdIQlc'
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

""" ************ User Management views ************ """

@users.route("/initialize_profile", methods=["POST"])
def create_profile():
    user = get_user(request.headers.get("Authorization", ""))
    profile = get_or_create_profile(user)
    return jsonify({"success": True, "profile": profile}), 200

@users.route("/profile", methods=["GET", "POST"])
def profile():
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 400
    profile = get_or_create_profile(user)
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
        profile.update({"username": data.get("username")})
        profile.update({"bio": data.get("bio")})
        profile.update({"profile_picture_uri": data.get("profile_picture_uri")})
        db.session.commit()
    return jsonify({"success": True, "profile": profile}), 200

@users.route("/favorites", methods=["GET"])
def favorites(): 
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 400
    profile = get_or_create_profile(user)
    if not profile.liked_posts:
        return jsonify({"success": True, "empty": True}), 200
    return jsonify({"success": True, "liked_posts": profile.liked_posts}), 200

@users.route("/comments", methods=["GET"])
def comments():
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 400
    profile = get_or_create_profile(user)
    if not profile.commented_posts:
        return jsonify({"success": True, "empty": True}), 200
    return jsonify({"success": True, "commented_posts": profile.commented_posts}), 200

@users.route("/settings", methods=["GET", "POST"])
def settings():
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 400
    profile = Profile.query.filter_by(user_id = user.id).first()
    if request.data:
        data = request.get_json()
        #Light/Dark Mode and Language Preferences will be buttons or dropdowns, no need for Forms
        if data.get("light_mode") is not None:
            profile.update({"light_mode": data.get("light_mode")})
        if data.get("language") is not None:    
            profile.update({"language": data.get("language")})
        db.session.commit()
    return jsonify({"success": True, "profile": profile}), 200

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