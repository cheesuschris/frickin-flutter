pub use crate::sup::*;
use chrono::{DateTime, Utc};
use flutter_rust_bridge::frb;
use serde::{Deserialize, Serialize};

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
    pub fn changePrivPub(&mut self) {
        self.privateProfileEnabled = !self.privateProfileEnabled;
    }
    pub fn changeNotifs(&mut self) {
        self.notificationsEnabled = !self.notificationsEnabled;
    }
}
