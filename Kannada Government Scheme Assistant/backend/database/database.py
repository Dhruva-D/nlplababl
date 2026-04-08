import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Load secure environment variables
load_dotenv()

# This pulls your secure connection URL from the hidden .env file so it never gets exposed online.
MONGO_URL = os.getenv("MONGO_URI")

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
