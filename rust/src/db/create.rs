use crate::sup::*;
user flutter::flutter_rust_bridge::frb;
#[flutter_rust_bridge::frb]
pub fn new_post(uid: String, recipe: String, cap: String, image: String) {
    post = Post::new(recipe, image, Vec<String>::new(), cap);
    user(uid).add_post(post);
}
#[flutter_rust_bridge::frb]
pub fn new_user(id: String, username: String, pic: String, bio: String, about: String) {
    user = User::new(id, username, pic, bio, about);

}
