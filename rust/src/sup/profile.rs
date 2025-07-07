// use chrono::{DateTime, Utc};
// use flutter_rust_bridge::frb;
// use serde::{Deserialize, Serialize};

use crate::sup::*;

impl Profile {
    pub fn new(
        user: User,
        followers: Vec<User>,
        following: Vec<User>,
        mutuals: Vec<User>,
        bookmarks: Vec<Post>,
        displayProfilePosts: Vec<Post>,
        settings: Settings,
        follower_count: i32,
        following_count: i32,
        verified_enabled: bool,
    ) -> Profile {
        Profile {
            user,
            followers,
            following,
            mutuals,
            bookmarks,
            displayProfilePosts,
            settings,
            verified_enabled,
            follower_count,
            following_count,
        }
    }
    pub fn new_following(&mut self, user1: User) {
        self.following.push(user1);
        self.inc_following();
    }
    pub fn new_follower(&mut self, user1: User) {
        self.followers.push(user1);
        self.inc_follower();
    }

    fn inc_follower(&mut self) {
        self.follower_count += 1;
    }
    fn inc_following(&mut self) {
        self.following_count += 1;
    }
}
