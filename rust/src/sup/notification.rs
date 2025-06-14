use crate::sup::*;
use chrono::{DateTime, Utc};

impl Notification {
    pub fn new(
        notificationId: String,
        to_user_id: String,
        from_user_id: String,
        message: String,
    ) -> Notification {
        Notification {
            notificationId: notificationId,
            to_user_id: to_user_id,
            from_user_id: from_user_id,
            message: message,
            read: false,
            createdAtTimeStamp: Utc::now(),
        }
    }
    pub fn opened(&mut self) {
        self.read = true;
    }
}
