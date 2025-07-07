use crate::sup::*;
use chrono::Utc;
impl User {
    pub fn new(
        user_id: String,
        username: String,
        profilePicture: String,
        posts: Vec<Post>,
        bio: String,
        about: String,
    ) -> User {
        User {
            user_id: user_id,
            username: username,
            profilePicture: profilePicture,
            posts: posts,
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
