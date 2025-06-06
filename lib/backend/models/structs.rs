use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};

#[derive(Debug, Serialize, Deserialize)]
struct User {
    pub userId: String,
    pub username: String,
    pub profilePicture: String,
    pub posts: Vec<Post>,
    pub bio: String,
    pub about: String,
    pub privateProfileEnabled: bool
    pub useerCreated: DateTime<Utc>
}

#[derive(Debug, Serialize, Deserialize)]
struct Profile {
    pub user: User,
    pub followers: Vec<User>,
    pub following: Vec<User>,
    pub mutuals: Vec<User>,
    pub bookmarks: Vec<Post>,
    pub displayProfilePosts: Vec<Post>,
    pub settings: Setings,
    pub verifiedEnabled: bool,
    pub followerCount: i32,
    pub followingCount: i32
}

#[derive(Debug, Serialize, Deserialize)]
struct Settings {
    pub multiFactorAuthEnabled: bool,
    pub privateProfileEnabled: bool,
    pub notificationsEnabled: bool
}

#[derive(Debug, Serialize, Deserialize)]
struct Notifications {
    pub notificationId: String,
    pub to_user_id: String,
    pub from_user_id: String,
    pub message: String,
    pub read: bool,
    pub createdAtTimeStamp: DateTime<Utc>
}

#[derive(Debug, Serialize, Deserialize)]
struct Auth {
    pub userID: String,
    pub hashedPassword: String,
    pub mfaSecret: Option<String>,
    pub mfaVerified: bool
}

#[derive(Debug, Serialize, Deserialize)]
struct Post {
    recipe: String,
    initRecipeImage: String,
    allImageFollowUpsToCompare: Vec<String>,
    timeStamp: DateTime<Utc>,
    caption: String
}