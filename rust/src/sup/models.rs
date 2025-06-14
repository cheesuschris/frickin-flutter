use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize)]
pub struct User {
    pub userId: String,
    pub username: String,
    pub profilePicture: String,
    pub posts: Vec<Post>,
    pub score: f32,
    pub bio: String,
    pub about: String,
    pub privateProfileEnabled: bool,
    pub userCreated: DateTime<Utc>,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct Profile {
    pub user: User,
    pub followers: Vec<User>,
    pub following: Vec<User>,
    pub mutuals: Vec<User>,
    pub bookmarks: Vec<Post>,
    pub displayProfilePosts: Vec<Post>,
    pub settings: Settings,
    pub verifiedEnabled: bool,
    pub followerCount: i32,
    pub followingCount: i32,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct Settings {
    pub multiFactorAuthEnabled: bool,
    pub privateProfileEnabled: bool,
    pub notificationsEnabled: bool,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct Notification {
    pub notificationId: String,
    pub to_user_id: String,
    pub from_user_id: String,
    pub message: String,
    pub read: bool,
    pub createdAtTimeStamp: DateTime<Utc>,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct Auth {
    pub userID: String,
    pub hashedPassword: String,
    pub mfaSecret: Option<String>,
    pub mfaVerified: bool,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct Post {
    pub recipe: String,
    pub initRecipeImage: String,
    pub ratingcount: i32,
    pub avgDiffRating: f32,
    pub avgTasteRating: f32,
    pub avgCostRating: f32,
    pub allImageFollowUpsToCompare: Vec<String>,
    pub timeStamp: DateTime<Utc>,
    pub caption: String,
    pub score: f32,
}
