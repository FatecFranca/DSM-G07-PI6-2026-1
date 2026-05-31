"""
JWT Authentication middleware and decorator for FastAPI.
Validates JWT tokens from incoming requests.
"""

from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Tuple
from app.application.services.jwt_service import jwt_service

oauth2_scheme = HTTPBearer()

async def verify_jwt_token(auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme)) -> Tuple[str, str]:
    """
    Dependency function to verify JWT token from Authorization header using HTTPBearer.
    """
    token = auth.credentials

    # Validate the token
    if not jwt_service.validate_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract user ID from token
    user_id = jwt_service.extract_user_id(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id, token


async def get_current_user(credentials: Tuple[str, str] = Depends(verify_jwt_token)) -> Tuple[str, str]:
    """
    Dependency function to get the current authenticated user and token.

    Args:
        credentials: A tuple of (user_id, token) from verify_jwt_token

    Returns:
        Tuple[str, str]: A tuple of (user_id, token)
    """
    return credentials



