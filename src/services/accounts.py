import uuid

from fastapi import HTTPException, status

from src.exceptions.security import BaseSecurityError
from src.security.token_manager import JWTAuthManagerInterface


def get_user_id_or_unauthorized(jwt_manager: JWTAuthManagerInterface, token: str) -> uuid.UUID:
    try:
        payload = jwt_manager.decode_access_token(token)
        user_id = payload.get("user_id")
    except BaseSecurityError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

    return user_id
