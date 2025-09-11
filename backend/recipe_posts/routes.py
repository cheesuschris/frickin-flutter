from flask import Blueprint, request, jsonify
from supabase import create_client
from ..forms import CreateRecipeForm, CommentForm
from ..models import db, Post, Notification, Profile, User, Comment
from utils import current_time

recipe_posts = Blueprint("recipe_posts", __name__)

# Creating a Supabase client instance
SUPABASE_URL = 'https://egdumlkkfxknccmvgzxo.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVnZHVtbGtrZnhrbmNjbXZnenhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc5Njk2MDEsImV4cCI6MjA2MzU0NTYwMX0.9yT_wv-72Hlea4E0Rlo4p8V_aWObnvxksx1UOTdIQlc'
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

""" ************ Recipe Post views ************ """

"""Post level routes"""

#TODO add tags to a post
@recipe_posts.route("/post", methods=["POST"])
def post():
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    profile = get_or_create_profile(user)
    if request.data:
        data = request.get_json()
        recipe_form = CreateRecipeForm({"title": data.get("title"), "recipe": data.get("recipe"), "image": data.get("image"), "tags": data.get("tags")})
        if not recipe_form.validate():
            return jsonify({"success": False, "error": recipe_form.errors}), 400
        post = Post(user_id = user.id, title = data.get("title"), recipe = data.get("recipe"), image_uri = data.get("image"), tags = data.get("tags"), timestamp = current_time(), likes_count = 0)
        db.session.add(post)
        db.session.flush()
        notifications = []
        for follower in profile.followers:
            notif = Notification(
                notified_id=follower.id,  
                post_id=post.id, 
                type="new_post", 
                message=f"{profile.username} has created a new post!", 
                timestamp=current_time()
            )
            notifications.append(notif)
        db.session.add_all(notifications)
        db.session.commit() 
        return jsonify({
            "success": True, 
            "message": f"Post created and {len(notifications)} followers notified",
            "post_id": post.id
        }), 200
    else:
        return jsonify({"success": False, "error": "empty post cuh"}), 400

@recipe_posts.route("/post/<int:post_id>", methods=["GET"])
def view_post(post_id):
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    post = Post.query.get(post_id)
    if post:
        return jsonify({"success": True, "post": post}), 200
    else:
        return jsonify({"success": False, "error": "ts don't exist"}), 404

@recipe_posts.route("/post/<int:post_id>", methods=["PUT"])
def edit_post(post_id):
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    if request.data:
        data = request.get_json()
        recipe_form = CreateRecipeForm({"title": data.get("title"), "recipe": data.get("recipe"), "image": data.get("image"), "tags": data.get("tags")})
        if not recipe_form.validate():
            return jsonify({"success": False, "error": recipe_form.errors}), 400
        post = Post.query.get(post_id)
        if not post:
            return jsonify({"success": False, "error": "post not found"}), 404
        if post.user_id != user.id:
            return jsonify({"success": False, "error": "unauthorized buddy"}), 400
        post.title = data.get("title")
        post.recipe = data.get("recipe")
        post.image = data.get("image")
        post.tags = data.get("tags")
        post.timestamp = current_time()
        db.session.commit()
        return jsonify({"success": True, "edited_post": post}), 200
    else:
        return jsonify({"success": False, "error": "fill in the blanks bro"}), 404

@recipe_posts.route("/post/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 400
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"success": False, "error": "post not found"}), 404
    if post.user_id != user.id:
        return jsonify({"success": False, "error": "unauthorized buddy"}), 400
    db.session.delete(post)
    db.session.commit()
    return jsonify({"success": True}), 200

#TODO add notifications
@recipe_posts.route("/post/<int:post_id>/toggle_like", methods=["PUT"])
def toggle_like_on_post(post_id):
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    profile = get_or_create_profile(user)
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"success": False, "error": "post not found"}), 404
    if post.user_id == user.id:
        return jsonify({"success": False, "error": "im crine bro liked his own post😹😹😹"}), 400
    if profile.has_liked_post(post):
        profile.like_post(post)
        db.session.commit()
    else:
        profile.unlike_post(post)
        db.session.commit()
    return jsonify({"success": True, "like_count": post.like_count, "liked_by": post.liked_by}), 200

@recipe_posts.route("/post/<int:post_id>/likes", methods=["GET"])
def get_all_likes(post_id):
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"success": False, "error": "post not found"}), 404
    return jsonify({"success": True, "like_count": post.like_count, "liked_by": post.liked_by}), 200

#TODO add notifications
@recipe_posts.route("/posts/<int:post_id>/comment", methods=["POST"])
def comment(post_id):
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    profile = get_or_create_profile(user)
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"success": False, "error": "post not found"}), 404
    if request.data:
        data = request.get_json()
        comment_form = CommentForm(text = data.get("comment"))
        if not comment_form.validate:
            return jsonify({"success": False, "error": comment_form.errors}), 400
        profile.comment_on_post(post, data.get("content"))
        return jsonify({"success": True, "comment": comment}), 200
    else:
        return jsonify({"success": False, "error": "Fill in the blanks bro"}), 404
    
@recipe_posts.route("/posts/<int:post_id>/comment/<int:comment_id>", methods=["GET"])
def get_comment(post_id, comment_id):
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"success": False, "error": "no comment luh bruh"}), 404
    return jsonify({"success": True, "comment": comment}), 200

@recipe_posts.route("/posts/<int:post_id>/comment/<int:comment_id>", methods=["PUT"])
def edit_comment(post_id, comment_id):
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"success": False, "error": "post not found"}), 404
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"success": False, "error": "comment not found"}), 404
    profile = get_or_create_profile(user)
    if comment.profile_id != profile.id:
        return jsonify({"success": False, "error": "unauthorized buddy"}), 400
    if request.data:
        data = request.get_json()
        comment_form = CommentForm(text = data.get("comment"))
        if not comment_form.validate:
            return jsonify({"success": False, "error": comment_form.errors}), 400
        comment.content = data.get("comment")
        db.session.commit()
        return jsonify({"success": False, "comment": comment}), 200
    else:
        return jsonify({"success": False, "error": "nothing there blud"}), 404

@recipe_posts.route("/posts/<int:post_id>/comment/<int:comment_id>", methods=["DELETE"])
def delete_comment(post_id, comment_id):
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    profile = get_or_create_profile(user)
    profile.delete_comment_on_post(comment_id)
    return jsonify({"success": True}), 200

@recipe_posts.route("/posts/<int:post_id>/comments", methods=["GET"])
def get_all_comments(post_id):
    user = get_user(request.headers.get("Authorization", ""))
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"success": False, "error": "post not found"}), 404
    comments = post.comments
    return jsonify({"success": True, "comments": comments}), 200

"""General recipe_posts level routes (not user feed)"""

#TODO everything below
@recipe_posts.route("/search", methods=["GET"])
def search():
    #Will search for both users and posts, UI would have tabs to switch between search filters
    print("Kenny do elastic search with this")

"""
# Discovery
GET    /recipe_posts/search?q=chicken        # Search recipes
GET    /recipe_posts/category               # Dietary preference recipes
GET    /recipe_posts/trending               # Trending recipes
GET    /recipe_posts/recent                 # Recent recipes
GET    /recipe_posts/random                 # Random recipe

# Categories
GET    /recipe_posts/categories             # All categories
GET    /recipe_posts/category/breakfast     # Breakfast recipes
"""

""" ************ Helper functions ************ """

def get_user(auth_header):
    token = auth_header.replace("Bearer ", "")
    user_response = supabase.auth.get_user(token)
    auth_user = user_response.user
    db_user = User.query.filter_by(id=auth_user.id).first()
    return db_user

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