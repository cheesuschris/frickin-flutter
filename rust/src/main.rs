use mongodb::{Client, options::ClientOptions};
use std::env;

#[tokio::main]
async fn main() -> mongodb::error::Result<()> {
    dotenv::from_filename("../assets/backend/credentials/.env").ok();
    // this loads the .env file in the credentials folder
    let uri = env::var("MONGO_CONNECTION_STRING").expect("so credentials was modified. who touched it.");
    //uri is now set
    let mut client_options = ClientOptions::parse(&uri).await?;
    //mongo_client_options created
    client_options.app_name = Some("CheeseCookingApp".to_string());
    //app name created
    let client = Client::with_options(client_options)?;
    //mongo_client created
    let db = client.database("cooking_database");
    //db accessed

    //DB Collections are as follows:
    //Auth
    //Notifications
    //Posts
    //Profile
    //user_bookmarks

    println!("MongoDB connection is stable");
    println!("Main is up and running");
    Ok(()) //needed since return value is a Result
}
