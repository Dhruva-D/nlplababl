import asyncio
import sys
import os

# Add the current directory to sys.path so we can import from 'database' and 'models'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import get_database
from models.scheme import SchemeModel

# Our sample data array matching the SchemeModel requirements
sample_schemes = [
    {
        "scheme_name": "Gruha Lakshmi",
        "description": "Provides financial assistance of Rs. 2,000 per month to the eligible female head of the family to support livelihood.",
        "keywords": ["women", "financial assistance", "cash transfer", "housewife"],
        "embedding": []
    },
    {
        "scheme_name": "Anna Bhagya",
        "description": "Provides 10 kg of free rice per person per month to BPL and Antyodaya card holders, or a direct cash transfer equivalent to the rice amount.",
        "keywords": ["food", "rice", "ration", "bpl", "cash transfer", "poverty"],
        "embedding": []
    },
    {
        "scheme_name": "Gruha Jyothi",
        "description": "Provides up to 200 units of free electricity per month to all residential households in Karnataka, reducing the burden of utility bills.",
        "keywords": ["electricity", "power", "free units", "utility bill", "energy"],
        "embedding": []
    },
    {
        "scheme_name": "Shakti",
        "description": "Offers free bus travel for women and transgender people across non-premium state-run buses within Karnataka.",
        "keywords": ["travel", "bus ticket", "women", "transport", "free travel"],
        "embedding": []
    },
    {
        "scheme_name": "Yuva Nidhi",
        "description": "Unemployment benefit of Rs. 3,000 per month for graduates and Rs. 1,500 per month for diploma holders for up to two years after graduation.",
        "keywords": ["youth", "unemployment", "graduates", "allowance", "students", "jobs"],
        "embedding": []
    }
]

async def seed_db():
    print("Connecting to Database...")
    db = get_database()
    
    # We will store our schemes in a collection named "schemes"
    collection = db["schemes"]
    
    # [Optional] Clear out existing schemes so we don't create duplicates when testing
    await collection.delete_many({})
    print("Cleared existing schemes from the collection.")
    
    # Validate the raw Python dictionaries against our Pydantic SchemeModel
    schemes_to_insert = []
    for scheme_dict in sample_schemes:
        # SchemeModel(**scheme_dict) ensures that all required fields exist and are of correct types
        valid_model = SchemeModel(**scheme_dict)
        # Convert it back to a dictionary so MongoDB can store it
        schemes_to_insert.append(valid_model.model_dump())
        
    if schemes_to_insert:
        # Perform the actual insert into the database
        await collection.insert_many(schemes_to_insert)
        print(f"✅ Successfully seeded {len(schemes_to_insert)} schemes into MongoDB!")

if __name__ == "__main__":
    # Run the asynchronous seeding function
    asyncio.run(seed_db())
