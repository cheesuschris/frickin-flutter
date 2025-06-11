use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};
use flutter_rust_bridge::frb;
mod models;
pub use models::*;

impl Profile {
    pub fn new(user: User, followers: Vec<User>, following: Vec<User>, 
    mutuals: Vec<User>, bookmarks: Vec<Post>, displayProfilePosts: Vec<Post>,
    settings: Settings, verifiedEnabled: bool) -> Profile {
        Profile {
            user,
            followers: Vec<User>::new(),
            following: Vec<User>::new(),
            mutuals: Vec<User>::new(),
            bookmarks: Vec<Post>::new(),
            displayProfilePosts: Vec<Post>::new(),
            settings: Settings,
            verifyEnabled: true,
            followerCount: 0,
            followingCount: 0
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
        self.followingCount +=1;
    }
}