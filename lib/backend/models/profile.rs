use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};

use super::user::User;
use super::settings::Settings;
impl Profile {
    pub fn new(user: User, followers: Vec<User> following: Vec<User>, 
    mutuals: Vec<User>, bookmarks: Vec<Post>, displayProfilePosts: Vec<Post>,
    settings: Settings, verifiedEnabled: bool) -> Profile {
        Profile {
            user,
            followers: mut Vec<User>,
            following: mut Vec<User>,
            mutuals: mut Vec<User>,
            bookmarks: mut Vec<Post>,
            displayProfilePosts: Vec<Post>
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