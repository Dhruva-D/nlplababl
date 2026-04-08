from fastapi import APIRouter
from pydantic import BaseModel
from database.database import get_database
from utils.nlp import generate_embedding
from utils.search import find_most_relevant_scheme

router = APIRouter()

class SearchQuery(BaseModel):
    text: str

@router.post("/search")
async def search_schemes(query: SearchQuery):
    """
    1. Receives Kannada text from React.
    2. Converts it into an AI vector embedding.
    3. Fetches all schemes from MongoDB.
    4. Finds the highest cosine-similarity match.
    5. Returns the best scheme back to React.
    """
    try:
        # Generate the math vector for the user's sentence
        user_vector = generate_embedding(query.text)
    except Exception as e:
        return {"error": f"Model failed: {str(e)}"}
        
    db = get_database()
    collection = db["schemes"]
    
    # Retrieve all schemes. In a production app with 1M rows, we would use a vector DB index.
    # For an academic project 5-50 schemes, fetching all and doing in-memory math is perfect!
    all_schemes = await collection.find({}).to_list(length=None)
    
    best_match = find_most_relevant_scheme(user_vector, all_schemes)
    
    # Clean MongoDB ObjectId so it sends properly in JSON
    if best_match and "_id" in best_match:
        best_match["_id"] = str(best_match["_id"])
        
    return {"result": best_match}
