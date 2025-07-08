use crate::sup::*;
use flutter::flutter_rust_bridge::frb;
use mongodb::{Collection, bson::doc};
#[flutter_rust_bridge::frb]
pub fn new_post(uid: String, recipe: String, cap: String, image: String) {
    let user = User{uid};
}
#[flutter_rust_bridge::frb]
pub fn new_user(id: String, username: String, pic: String, bio: String, about: String) {
    let user = User::new(id, username, pic, bio, about);

}
