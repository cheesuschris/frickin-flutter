use crate::sup::*;
use chrono::{DateTime, Utc};
impl User {
    pub fn new(
        userId: String,
        username: String,
        profilePicture: String,
        posts: Vec<Post>,
        bio: String,
        about: String,
    ) -> User {
        User {
            userId: userId,
            username: username,
            profilePicture: profilePicture,
            posts: posts,
            score: 0.0,
            bio: bio,
            about: about,
            privateProfileEnabled: false,
            userCreated: Utc::now(),
        }
    }
}
