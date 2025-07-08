use crate::sup::*;
use chrono::Utc;
// use flutter_rust_bridge::frb;
// use serde::{Deserialize, Serialize};
use mongodb::{Collection, bson::doc};

impl Post {
    pub fn new(
        recipe: String,
        init_recipe_image: String,
        all_image_follow_ups_to_compare: Vec<String>,
        caption: String,
    ) -> Post {
        Post {
            recipe: recipe,
            init_recipe_image: init_recipe_image,
            rating_count: 0,
            avg_diff_rating: 0.0,
            avg_taste_rating: 0.0,
            avg_cost_rating: 0.0,
            all_image_follow_ups_to_compare,
            time_stamp: Utc::now(),
            caption: caption,
            score: 0.0,
        }
    }
    pub fn set_cap(&mut self, cap: String) {
        self.caption = cap;
    }
    pub fn set_rec(&mut self, rec: String) {
        self.recipe = rec;
    }
    pub fn reset_time(&mut self) {
        self.time_stamp = Utc::now();
    }
    pub fn set_img(&mut self, url: String) {
        self.init_recipe_image = url;
    }
    fn inc_rating_count(&mut self) {
        self.rating_count += 1;
    }
    fn avg_change(&mut self, diff: f32, taste: f32, cost: f32) {
        self.avg_diff_rating = (self.avg_diff_rating * self.rating_count as f32 + diff)
            / (self.rating_count as f32 + 1.0);
        self.avg_cost_rating = (self.avg_cost_rating * (self.rating_count as f32) + cost)
            / ((self.rating_count as f32) + 1.0);
        self.avg_taste_rating = (self.avg_taste_rating * (self.rating_count as f32) + taste)
            / ((self.rating_count as f32) + 1.0);
        self.inc_rating_count();
    }
    fn score_calc() {
        // needs impl
    }
}
