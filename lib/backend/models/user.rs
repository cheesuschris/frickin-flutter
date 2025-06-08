use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};
use flutter_rust_bridge::frb;
mod models;
pub use models::*;

#[frb]
impl User {
    pub fn new(userID: String, username:String, profilePicture:String, 
            posts: Vec<Post>, followers: Vec<String>, following: Vec<String>, 
            mutuals: Vec<String>, bio: String, score: f32, about: String, 
            privateProfileEnabled: bool, userCreated: DateTime<Utc>) -> User{
        User {
            userId,
            username,
            profilePicture,
            posts: mut Vec::new(),
            score: 0.0,
            bio,
            about,
            privateProfileEnabled: mut false,
            userCreated: Utc::now()
        }
    }
}