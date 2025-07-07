use crate::sup::*;
use chrono::Utc;

impl Notification {
    pub fn new(
        notification_id: String,
        to_user_id: String,
        from_user_id: String,
        message: String,
    ) -> Notification {
        Notification {
            notification_id: notification_id,
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
