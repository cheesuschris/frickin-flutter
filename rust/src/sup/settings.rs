pub use crate::sup::*;
use chrono::{DateTime, Utc};
use flutter_rust_bridge::frb;
use serde::{Deserialize, Serialize};

impl Settings {
    pub fn new(
        multiFactorAuthEnabled: bool,
        privateProfileEnabled: bool,
        notificationsEnabled: bool,
    ) -> Settings {
        Settings {
            multiFactorAuthEnabled,
            privateProfileEnabled,
            notificationsEnabled,
        }
    }
}
