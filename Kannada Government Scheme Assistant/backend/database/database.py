from motor.motor_asyncio import AsyncIOMotorClient

# This is your MongoDB connection URL. 
# By default, "mongodb://localhost:27017" connects to a MongoDB server running locally on your PC.
MONGO_URL = "mongodb+srv://corsit:clubofrobotics2023@corsit.q9mskze.mongodb.net/?retryWrites=true&w=majority"

# These variables will hold our database connection
client = None
database = None

def get_database():
    """
    Returns the MongoDB database instance.
    You can import this function in any file where you need to save or read data.
    """
    global client, database
    
    # Initialize the client only if it hasn't been set up yet
    if client is None:
        client = AsyncIOMotorClient(MONGO_URL)
        # Give our database a name: "authnlp"
        database = client["authnlp"]
        print("✅ Successfully connected to MongoDB!")
        
    return database
