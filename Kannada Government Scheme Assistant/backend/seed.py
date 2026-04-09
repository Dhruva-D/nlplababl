import asyncio
import sys
import os

# Add the current directory to sys.path so we can import from 'database' and 'models'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import get_database
from models.scheme import SchemeModel
from utils.nlp import generate_embedding

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
    },
    {
        "scheme_name": "Mathrushree Scheme",
        "description": "Provides financial assistance of Rs. 6,000 to pregnant women belonging to BPL families to help cover medical expenses and ensure proper nutrition during pregnancy and lactation.",
        "keywords": ["pregnancy", "maternity", "women", "bpl", "nutrition", "health"],
        "embedding": []
    },
    {
        "scheme_name": "Raitha Vidya Nidhi",
        "description": "A scholarship program for the children of farmers, agricultural laborers, and weavers to encourage them to pursue higher education.",
        "keywords": ["farmers", "agriculture", "scholarship", "education", "students", "children"],
        "embedding": []
    },
    {
        "scheme_name": "Ganga Kalyana Scheme",
        "description": "Provides irrigation facilities through borewells or open wells to farmers belonging to Scheduled Castes and Scheduled Tribes to improve agricultural productivity.",
        "keywords": ["irrigation", "borewell", "sc/st", "farmers", "agriculture", "water"],
        "embedding": []
    },
    {
        "scheme_name": "Bhagyalakshmi Scheme",
        "description": "Promotes the birth of girl children in below poverty line (BPL) families by providing financial assistance through bonds that mature when the girl turns 18.",
        "keywords": ["girl child", "bpl", "savings", "women empowerment", "financial assistance"],
        "embedding": []
    },
    {
        "scheme_name": "Sandhya Suraksha Yojana",
        "description": "A social security scheme providing a monthly pension of Rs. 1,200 to senior citizens (aged 65 and above) from weaker sections to ensure their financial security.",
        "keywords": ["pension", "senior citizens", "old age", "elderly", "social security"],
        "embedding": []
    },
    {
        "scheme_name": "Arivu Education Loan Scheme",
        "description": "An educational loan scheme offering financial assistance at a low interest rate (2%) to students from religious minority communities pursuing professional courses.",
        "keywords": ["education loan", "minority", "students", "professional course", "financial aid"],
        "embedding": []
    },
    {
        "scheme_name": "Chief Minister's Employment Generation Programme (CMEGP)",
        "description": "Provides subsidies and margin money to rural and urban youth for setting up new micro-enterprises to promote self-employment and entrepreneurship.",
        "keywords": ["business", "subsidy", "youth", "entrepreneurship", "employment", "micro-enterprise"],
        "embedding": []
    },
    {
        "scheme_name": "Vidya Siri Scheme",
        "description": "Provides a monthly stipend of Rs. 1,500 for food and accommodation to backward class students pursuing post-matric courses who have not secured admission to state-run hostels.",
        "keywords": ["student", "hostel", "stipend", "backward classes", "education", "allowance"],
        "embedding": []
    },
    {
        "scheme_name": "PM-KISAN with State Top-up (Karnataka)",
        "description": "Provides an annual income support of Rs. 6,000 from the Central Government and an additional Rs. 4,000 from the Karnataka State Government to all eligible landholding farmer families.",
        "keywords": ["farmers", "income support", "cash transfer", "agriculture", "landholding"],
        "embedding": []
    },
    {
        "scheme_name": "Ayushman Bharat - Arogya Karnataka",
        "description": "A unified health insurance scheme providing free or highly subsidized universal health coverage for catastrophic illnesses to all residents of Karnataka.",
        "keywords": ["health", "insurance", "hospital", "medical", "universal health", "illness"],
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
        print(f"Generating AI embeddings for {scheme_dict['scheme_name']}...")
        # Create vectors based on the description
        scheme_dict["embedding"] = generate_embedding(scheme_dict["description"])
        
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
