from flask import Blueprint, request, jsonify
from supabase import create_client
from ..forms import CreateRecipeForm

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
        return jsonify({"error": "User not found"}), 404
    #Connect to database and get user profile information
    #If POST, use forms and update databases

@users.route("/favorites", methods=["GET", "POST"])
def favorites(): 
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    user_response = supabase.auth.get_user(token)
    user = user_response.user
    if not user:
        return jsonify({"error": "User not found"}), 404
    #Connect to database and get user's favorite posts

@users.route("/settings", methods=["GET", "POST"])
def settings():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    user_response = supabase.auth.get_user(token)
    user = user_response.user
    if not user:
        return jsonify({"error": "User not found"}), 404
    #Implement settings logic here