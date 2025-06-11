// src/models/mod.rs
pub mod models;
pub mod post;
pub mod profile;
pub mod user;

// Re-export everything so you can use it easily
pub use models::*;
pub use post::*;
pub use profile::*;
pub use user::*;
