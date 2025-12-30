from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Ecommerce.app.core.deps import get_db
from Ecommerce.app.core.security import decode_token
from Ecommerce.app.models import User
from Ecommerce.app.repository.UserRepository import UserRepository

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user_name = payload.get("sub")
    if user_name is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid payload",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_user_name(user_name)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid payload",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user

def require_roles(required_roles: list[str]):
    async def role_checker(user = Depends(get_current_user)):
        user_roles = [ur.role.code for ur in user.user_roles]
        if not any(role in user_roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )

        return user

    return role_checker