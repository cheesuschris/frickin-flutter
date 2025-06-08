use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};
use flutter_rust_bridge::frb;
mod models;
pub use models::*;

impl Post {
    pub fn new(recipe:String, initRecipeImage: String, ratingcount: i32, avgDiffRating: f32, avgTasteRating: f32, avgCostRating: f32, allImageFollowUpsToCompare: String, timeStamp: DateTime<Utc>, caption: Striing) -> Post{
        Post{
            recipe,
            initRecipeImage,
            ratingcount: 1,
            avgDiffRating: f32,
            avgTasteRating: f32,
            avgCostRating: f32,
            allImageFollowUpsToCompare,
            timeStamp: Utc::now(),
            caption,
            score: 0.0001
        }
    }
    pub fn setCap(&mut self, cap: String) {
        self.caption = cap;
    }
    pub fn setRec(&mut self, rec:String) {
        self.recipe = rec;
    }
    pub fn resetTime(&mut self) {
        self.timeStamp = Utc::now();
    }
    pub fn setImg(@mut self, url: String) {
        self.initRecipeImage = url;
    }
    fn incRatingCount(&mut self) {
        self.ratingcount+=1;
    }
    fn avgChange(&mut self, diff:f32, taste: f32, cost: f32) {
        self.avgDiffRating = (self.avgDiffRating*ratingcount+diff)/(ratingcount+1);
        self.avgCostRating = (self.avgCostRating*ratingcount+cost)/(ratingcount+1);
        self.avgTasteRating = (self.avgTasteRating*ratingcount+taste)/(ratingcount+1);
        self.incRatingCount();
    }
    fn scoreCalc() {
        
    }
}