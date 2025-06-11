use chrono::{DateTime, Utc};
use flutter_rust_bridge::frb;
use serde::{Deserialize, Serialize};
mod models;
pub use models::*;

impl Settings {
    pub fn new(
        multiFactorAuthEnabled: bool,
        privateProfileEnabled: bool,
        notificationsEnabled: bool,
    ) -> Settings {
        Settings {
            multiFactorAuthEnabled: false,
            privateProfileEnabled: false,
            notificationId: true,
        };
    }
}
