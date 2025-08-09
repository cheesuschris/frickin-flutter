pub use crate::sup::*;
// use chrono::{DateTime, Utc};
// use flutter_rust_bridge::frb;
// use serde::{Deserialize, Serialize};

impl Settings {
    pub fn new() -> Settings {
        Settings {
            multifactor_auth_enabled: false,
            private_profile_enabled: false,
            notifications_enabled: true,
        }
    }
    pub fn change_multi_auth(&mut self) {
        self.multifactor_auth_enabled = !self.multifactor_auth_enabled;
    }
    pub fn change_priv_pub(&mut self) {
        self.private_profile_enabled = !self.private_profile_enabled;
    }
    pub fn change_notifs(&mut self) {
        self.notifications_enabled = !self.notifications_enabled;
    }
}

impl Default for Settings {
    fn default() -> Self {
        Self::new()
    }
}
