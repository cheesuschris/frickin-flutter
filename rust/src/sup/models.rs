use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize)]
pub struct User {
    pub user_id: String,
    pub username: String,
    pub profile_picture: String,
    pub posts: Vec<Post>,
    pub score: f32,
    pub bio: String,
    pub about: String,
    pub private_profile_enabled: bool,
    pub user_created: DateTime<Utc>,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct Profile {
    pub user: User,
    pub followers: Vec<User>,
    pub following: Vec<User>,
    pub mutuals: Vec<User>,
    pub bookmarks: Vec<Post>,
    pub display_profile_posts: Vec<Post>,
    pub settings: Settings,
    pub verified_enabled: bool,
    pub follower_count: i32,
    pub following_count: i32,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct Settings {
    pub multifactor_auth_enabled: bool,
    pub private_profile_enabled: bool,
    pub notifications_enabled: bool,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct Notification {
    pub notification_id: String,
    pub to_user_id: String,
    pub from_user_id: String,
    pub message: String,
    pub read: bool,
    pub created_at_time_stamp: DateTime<Utc>,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct Auth {
    pub user_id: String,
    pub hashed_password: String,
    pub mfa_secret: Option<String>,
    pub mfa_verified: bool,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct Post {
    pub recipe: String,
    pub init_recipe_image: String,
    pub rating_count: i32,
    pub avg_diff_rating: f32,
    pub avg_taste_rating: f32,
    pub avg_cost_rating: f32,
    pub all_image_follow_ups_to_compare: Vec<String>,
    pub time_stamp: DateTime<Utc>,
    pub caption: String,
    pub score: f32,
}
