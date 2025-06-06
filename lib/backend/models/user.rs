use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};

use super::post::Post;
impl User {
    pub fn new(userID: String, username:String, profilePicture:String, 
            posts: Vec<Post>, followers: Vec<String>, following: Vec<String>, 
            mutuals: Vec<String>, bio: String, score: f32, about: String, 
            privateProfileEnabled: bool, userCreated: DateTime<Utc>) -> Self{
        User {
            userId,
            username,
            profilePicture,
            posts: mut Vec::new(),
            score: 0.0,
            bio,
            about,
            privateProfileEnabled: false,
            userCreated: Utc::now(),
        }
    }
}