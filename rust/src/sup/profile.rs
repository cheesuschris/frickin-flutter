use chrono::{DateTime, Utc};
use flutter_rust_bridge::frb;
use serde::{Deserialize, Serialize};

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
        followerCount: i32,
        followingCount: i32,
        verifiedEnabled: bool,
    ) -> Profile {
        Profile {
            user,
            followers,
            following,
            mutuals,
            bookmarks,
            displayProfilePosts,
            settings,
            verifiedEnabled,
            followerCount,
            followingCount,
        }
    }
    pub fn newfollowing(&mut self, user1: User) {
        self.following.push(user1);
        self.incFollowing();
    }
    pub fn newfollower(&mut self, user1: User) {
        self.followers.push(user1);
        self.incFollower();
    }

    fn incFollower(&mut self) {
        self.followerCount += 1;
    }
    fn incFollowing(&mut self) {
        self.followingCount += 1;
    }
}
