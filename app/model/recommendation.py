from pydantic import BaseModel

class RecommendationRequest(BaseModel):
    mood: str
    description: str