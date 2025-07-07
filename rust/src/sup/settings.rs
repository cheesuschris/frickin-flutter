pub use crate::sup::*;
// use chrono::{DateTime, Utc};
// use flutter_rust_bridge::frb;
// use serde::{Deserialize, Serialize};

impl Settings {
    pub fn new() -> Settings {
        Settings {
            multiFactorAuthEnabled: false,
            privateProfileEnabled: false,
            notificationsEnabled: true,
        }
    }
    pub fn changeMultiAuth(&mut self) {
        self.multiFactorAuthEnabled = !self.multiFactorAuthEnabled;
    }
    pub fn change_priv_pub(&mut self) {
        self.private_profile_enabled = !self.private_profile_enabled;
    }
    pub fn change_notifs(&mut self) {
        self.notifications_enabled = !self.notifications_enabled;
    }
}
