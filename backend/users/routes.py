from flask import Blueprint, request, jsonify
from supabase import create_client
from ..forms import CreateRecipeForm, UpdateUserNameForm, UpdateProfilePicForm, UpdateBioForm
from ..models import Profile, Notification
from . import db, current_time
from hashids import Hashids

users = Blueprint("users", __name__)

#Creating a supabase client instance
SUPABASE_URL = 'https://egdumlkkfxknccmvgzxo.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVnZHVtbGtrZnhrbmNjbXZnenhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc5Njk2MDEsImV4cCI6MjA2MzU0NTYwMX0.9yT_wv-72Hlea4E0Rlo4p8V_aWObnvxksx1UOTdIQlc'
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

""" ************ User Management views ************ """

@users.route("/profile", methods=["GET", "POST"])
def profile():
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    profile = get_or_create_profile(user)
    if request.method == "POST":
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
        else:
            return jsonify({"success": False, "error": "No data found"}), 404
    return jsonify({"success": True, "profile": profile}), 200

#profile_id, not user_id because later on we might have the user create multiple profiles and delete some as well
@users.route("/profile/<int:profile_id>", methods=["GET"])
def view_profile(profile_id):
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    profile_to_view = Profile.query.filter_by(id=profile_id).first()
    if not profile_to_view:
        return jsonify({"success": False, "error": "User profile you wish to see doesn't exist"}), 404
    return jsonify({"success": True, "profile": profile_to_view}), 200

@users.route("/profile/posts", methods=["GET"])
def get_posts():
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    profile = get_or_create_profile(user)
    posts = profile.posts
    return jsonify({"success": True, "posts": posts}), 200

@users.route("/profile/favorites", methods=["GET"])
def get_favorites(): 
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    profile = get_or_create_profile(user)
    posts = profile.liked_posts
    return jsonify({"success": True, "liked_posts": posts}), 200

@users.route("/profile/comments", methods=["GET"])
def get_comments():
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    profile = get_or_create_profile(user)
    posts = profile.commented_posts
    return jsonify({"success": True, "commented_posts": posts}), 200

@users.route("/profile/settings", methods=["GET", "POST"])
def additional_settings():
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    profile = Profile.query.filter_by(user_id = user.id).first()
    if request.method == "POST":
        if request.data:
            data = request.get_json()
            #Light/Dark Mode and Language Preferences will be buttons or dropdowns, no need for Forms
            if data.get("light_mode") is not None:
                profile.update({"light_mode": data.get("light_mode")})
            if data.get("language") is not None:    
                profile.update({"language": data.get("language")})
            db.session.commit()
        else:
            return jsonify({"success": False, "error": "No additional settings provided"}), 404
    return jsonify({"success": True, "profile": profile}), 200

@users.route("/profile/notifications", methods=["GET"])
def get_notifications():
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    profile = get_or_create_profile(user)
    unread_notifications = Notification.query.filter_by(
        notified_id=profile.id,
        read=False
    ).order_by(Notification.timestamp.desc()).limit(20).all()
    read_notifications = Notification.query.filter_by(
        notified_id = profile.id,
        read = True
    ).order_by(Notification.timestamp.desc()).limit(20).all()
    return jsonify({
        "success": True,
        "unread_notifications": [{
            "id": n.id,
            "type": n.type,
            "message": n.message,
            "post_id": n.post_id,
            "timestamp": n.timestamp.isoformat(),
            "read": n.read
        } for n in unread_notifications],
        "unread_count": len(unread_notifications),
        "read_notifications": [{
            "id": n.id,
            "type": n.type,
            "message": n.message,
            "post_id": n.post_id,
            "timestamp": n.timestamp.isoformat(),
            "read": n.read
        } for n in read_notifications],
        "read_count": len(read_notifications)
    }), 200

@users.route("/profile/notifications/<int:notif_id>/mark_read", methods=["POST"])
def mark_notification_read(notif_id):
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    profile = get_or_create_profile(user)
    notification = Notification.query.filter_by(
        id=notif_id,
        notified_id=profile.id
    ).first()
    if notification:
        notification.read = True
        db.session.commit()
        return jsonify({"success": True, "notification": notification}), 200
    return jsonify({"success": False, "error": "Notification not found"}), 404

@users.route("/profile/follow/<int:user_id>", methods=["POST"])
def follow_user(user_id):
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    profile = get_or_create_profile(user)
    target_profile = Profile.query.filter_by(user_id=user_id).first()
    if not target_profile:
        return jsonify({"success": False, "error": "User to follow not found"}), 404
    if profile.id == target_profile.id:
        return jsonify({"success": False, "error": "Cannot follow yourself"}), 400
    if profile.is_following(target_profile):
        return jsonify({"success": False, "error": "Already following this user"}), 400
    profile.follow(target_profile)
    db.session.commit()
    notif = Notification(
        notified_id=target_profile.id,
        type="new_follower",
        message=f"{profile.username} started following you!",
        timestamp=current_time()
    )
    db.session.add(notif)
    db.session.commit()
    return jsonify({
        "success": True,
        "message": f"Now following {target_profile.username}",
        "following_count": profile.following_count
    }), 200

@users.route("/profile/unfollow/<int:user_id>", methods=["DELETE"])
def unfollow_user(user_id):
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    profile = get_or_create_profile(user)
    target_profile = Profile.query.filter_by(user_id=user_id).first()
    if not target_profile:
        return jsonify({"success": False, "error": "User to unfollow not found"}), 404
    profile.unfollow(target_profile) #let this handle the user already being unfollowed
    db.session.commit()
    #Don't create notif for unfollow
    return jsonify({
        "success": True,
        "message": f"No longer following {target_profile.username}",
        "following_count": profile.following_count
    }), 200

@users.route("/profile/following", methods=["GET"])
def get_following():
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    profile = get_or_create_profile(user)
    following = [{
        "id": f.id,
        "user_id": f.user_id,
        "username": f.username,
        "profile_picture_uri": f.profile_picture_uri
    } for f in profile.following]
    return jsonify({
        "success": True,
        "following": following,
        "count": len(following)
    }), 200

@users.route("/profile/followers", methods=["GET"])
def get_followers():
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    profile = get_or_create_profile(user)
    followers = [{
        "id": f.id,
        "user_id": f.user_id,
        "username": f.username,
        "profile_picture_uri": f.profile_picture_uri
    } for f in profile.followers]
    return jsonify({
        "success": True,
        "followers": followers,
        "count": len(followers)
    }), 200

@users.route("/profile/change_password", method=["PUT"])
def change_password():
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    current_password = user.password_hash
    if request.data():
        data = request.get_json()
        old_password = data.get("old_password")
        if old_password != current_password:
            return jsonify({"success": False, "error": "Provided old password and current password do not match"}), 400
        else:
            new_password = data.get("new_password")
            try:
                supabase.auth.update_user({"password": new_password})
                return jsonify({"success": True, "new_password": new_password}), 200
            except Exception as e:
                error_msg = str(e).lower()
                client_errors = [
                    'weak_password', 'same_password', 'validation_failed',
                    'session_expired', 'session_not_found', 'reauthentication_needed'
                ]
                if any(code in error_msg for code in client_errors):
                    return jsonify({"success": False, "error": str(e)}), 400
                else:
                    return jsonify({"success": False, "error": str(e)}), 500 
    else:
        return jsonify({"success": False, "error": "No forms filled"}), 404

@users.route("/logout", method=["POST"])
def logout():
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    try:
        supabase.auth.sign_out()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

#TODO
@users.route("/profile/feed", methods=["GET"])
def get_feed():
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    profile = get_or_create_profile(user)
    followers = profile.followers
    following = profile.following
    #Get following and followers' recipes, filtered by unread and ordered by timestamp
    #Then randomly get explore page recipes

#TODO
# FOR THE FUTURE: Add collections and dietary_preferences routes, as well as maybe models for them as well

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