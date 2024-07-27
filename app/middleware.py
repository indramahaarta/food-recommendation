from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import HTTPException, status
from firebase_admin.auth import verify_id_token
import logging

class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Skip JWT verification for the root path
        if request.url.path == "/":
            response = await call_next(request)
            return response

        # Get the Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                # Extract the JWT token from the header
                token = auth_header.split("Bearer ")[1]
                # Verify the token
                verify_id_token(token)
            except Exception as e:
                logging.error(f"Error verifying token: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or missing JWT token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing JWT token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        response = await call_next(request)
        return response
