from fastapi import APIRouter
from pydantic import BaseModel
from database.database import get_database
from utils.nlp import generate_embedding
from utils.search import find_top_matching_schemes

router = APIRouter()

class SearchQuery(BaseModel):
    text: str

@router.post("/search")
async def search_schemes(query: SearchQuery):
    """
    1. Receives Kannada text from React.
    2. Converts it into an AI vector embedding.
    3. Fetches all schemes from MongoDB.
    4. Returns top 3 most similar schemes sorted by confidence score descending.
    """
    try:
        user_vector = generate_embedding(query.text)
    except Exception as e:
        return {"error": f"Model failed: {str(e)}"}

    db = get_database()
    collection = db["schemes"]

    # Fetch all schemes from MongoDB
    all_schemes = await collection.find({}).to_list(length=None)

    # Get top 3 matches that clear the minimum confidence threshold
    top_matches = find_top_matching_schemes(user_vector, all_schemes, top_n=3)

    # If nothing cleared the 40% threshold, tell the user clearly
    if not top_matches:
        return {
            "query": query.text,
            "total_results": 0,
            "results": [],
            "message": "No relevant government scheme found."
        }

    return {
        "query": query.text,
        "total_results": len(top_matches),
        "results": top_matches
    }
