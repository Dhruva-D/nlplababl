from pydantic import BaseModel, Field
from typing import List, Optional

class SchemeModel(BaseModel):
    """
    Pydantic Schema defining what a Scheme document looks like in MongoDB.
    """
    scheme_name: str = Field(..., description="The official name of the scheme (e.g., 'Gruha Lakshmi').")
    description: str = Field(..., description="A clear description of what the scheme provides to citizens.")
    keywords: List[str] = Field(..., description="A list of tags/keywords (e.g., ['women', 'finance']) to help in normal text searches.")
    
    # We make embeddings Optional because we might add them later using an AI model.
    # It will hold a list of floating point numbers representing the text's vector.
    embedding: Optional[List[float]] = Field(default=[], description="Vector embeddings for semantic AI search.")

    class Config:
        json_schema_extra = {
            "example": {
                "scheme_name": "Gruha Lakshmi",
                "description": "Financial assistance of Rs. 2000 to the female head of the family.",
                "keywords": ["finance", "women", "cash", "subsidy"],
                "embedding": [0.12, 0.45, -0.67]
            }
        }
