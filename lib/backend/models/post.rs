use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

impl Post {
    pub fn new(recipe:String, initRecipeImage: String, allImageFollowUpsToCompare: String, timeStamp: DateTime<Utc>, caption: Striing) -> Post{
        Post{
            recipe,
            initRecipeImage,
            allImageFollowUpsToCompare,
            timeStamp: Utc::now(),
            caption
        }
    }
    fn setCap(&mut self, cap: String) {
        self.caption = cap;
    }
    fn setRec(&mut self, rec:String) {
        self.recipe = rec;
    }
    fn resetTime(&mut self, time:Utc::now()) {
        self.timeStamp = 
    } 
}