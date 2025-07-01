use crate::sup::*;
#[flutter_rust_bridge::frb]
pub fn new_post(uid: String, recipe: String, cap: String, image: String) {
    post = Post::new(recipe, image, Vec<String>::new(), cap);
    user(uid).add_post(post);
}
#[flutter_rust_bridge::frb]
pub fn new_profile();