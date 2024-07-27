# app/router.py
from fastapi import APIRouter, Depends
from typing import Annotated
from app.config import get_firebase_user_from_token
from app.query.user import save_or_get_user_from_firestore
from app.model.recommendation import RecommendationRequest
from app.agent.response_generator import ResponseGenerator
from app.db import db  # Import the db object

router = APIRouter()

@router.get("/")
def hello():
    """Hello world route to make sure the app is working correctly"""
    return {"msg": "Hello World!"}

@router.get("/verify")
async def get_userid(user: Annotated[dict, Depends(get_firebase_user_from_token)]):
    """Gets the Firebase connected user and saves to Firestore"""
    saved_user = await save_or_get_user_from_firestore(db=db, user=user)
    return saved_user

@router.post("/recommendation")
async def create_item(req: RecommendationRequest):
    agent = ResponseGenerator()
    output = agent.generate_answer(db=db, question=f"Please provide the top food recommendations for people that feel {req.mood} and {req.description}")
    return {"recommendation": output, "total": len(output)}
