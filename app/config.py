import os
import traceback
import logging
import pathlib

from functools import lru_cache
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin.auth import verify_id_token

basedir = pathlib.Path(__file__).parents[1]
load_dotenv(basedir / ".env")
bearer_scheme = HTTPBearer(auto_error=False)

class Settings(BaseSettings):
    """Main settings"""
    app_name: str = "Grow Mood"
    env: str = os.getenv("ENV", "development")
    firebase_config_path: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY")

@lru_cache
def get_settings() -> Settings:
    """Retrieves the FastAPI settings"""
    return Settings()

def get_firebase_user_from_token(
    token: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> Optional[dict]:
    """Uses bearer token to identify firebase user id

    Args:
        token : the bearer token. Can be None as we set auto_error to False

    Returns:
        dict: the firebase user on success

    Raises:
        HTTPException 401 if user does not exist or token is invalid
    """
    try:
        if not token:
            raise ValueError("No token")
        user = verify_id_token(token.credentials)
        return user
    except Exception as e:
        logging.error(f"Error verifying token: {str(e)}")
        traceback.print_exc()
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not logged in or Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

