use crate::sup::Post;
use chrono::{DateTime, Utc};
use flutter_rust_bridge::frb;
use serde::{Deserialize, Serialize};

impl Post {
    pub fn new(
        recipe: String,
        initRecipeImage: String,
        allImageFollowUpsToCompare: Vec<String>,
        caption: String,
    ) -> Post {
        Post {
            recipe: recipe,
            initRecipeImage: initRecipeImage,
            ratingcount: 0,
            avgDiffRating: 0.0,
            avgTasteRating: 0.0,
            avgCostRating: 0.0,
            allImageFollowUpsToCompare,
            timeStamp: Utc::now(),
            caption: caption,
            score: 0.0,
        }
    }
    pub fn setCap(&mut self, cap: String) {
        self.caption = cap;
    }
    pub fn setRec(&mut self, rec: String) {
        self.recipe = rec;
    }
    pub fn resetTime(&mut self) {
        self.timeStamp = Utc::now();
    }
    pub fn setImg(&mut self, url: String) {
        self.initRecipeImage = url;
    }
    fn incRatingCount(&mut self) {
        self.ratingcount += 1;
    }
    fn avgChange(&mut self, diff: f32, taste: f32, cost: f32) {
        self.avgDiffRating =
            (self.avgDiffRating * self.ratingcount as f32 + diff) / (self.ratingcount as f32 + 1.0);
        self.avgCostRating = (self.avgCostRating * (self.ratingcount as f32) + cost)
            / ((self.ratingcount as f32) + 1.0);
        self.avgTasteRating = (self.avgTasteRating * (self.ratingcount as f32) + taste)
            / ((self.ratingcount as f32) + 1.0);
        self.incRatingCount();
    }
    fn scoreCalc() {}
}
