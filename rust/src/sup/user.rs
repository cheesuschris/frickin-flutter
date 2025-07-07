use crate::sup::*;
use chrono::Utc;
impl User {
    pub fn new(
        user_id: String,
        username: String,
        profile_picture: String,
        bio: String,
        about: String,
    ) -> User {
        User {
            user_id: user_id,
            username: username,
            profile_picture: profile_picture,
            posts: Vec::new(),
            score: 0.0,
            bio: bio,
            about: about,
            private_profile_enabled: false,
            user_created: Utc::now(),
        }
    }
    pub fn add_post(&mut self, post: Post) {
        self.posts.push(post);
    }
}
