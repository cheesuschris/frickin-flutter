use crate::models::Post;
use crate::models::User;
use chrono::{DateTime, Utc};
impl User {
    pub fn new(
        userId: String,
        username: String,
        profilePicture: String,
        posts: Vec<Post>,
        followers: Vec<String>,
        following: Vec<String>,
        mutuals: Vec<String>,
        bio: String,
        score: f32,
        about: String,
        privateProfileEnabled: bool,
        userCreated: DateTime<Utc>,
    ) -> User {
        User {
            userId,
            username,
            profilePicture,
            posts: Vec::new(),
            score: 0.0,
            bio,
            about,
            privateProfileEnabled: false,
            userCreated: Utc::now(),
        }
    }
}
