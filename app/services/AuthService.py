from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession

from Ecommerce.app import db
from Ecommerce.app.converter.AuthConverter import to_user_entity
from Ecommerce.app.converter.AuthConverter import to_user_response
from Ecommerce.app.core.security import verify_password, create_access_token, create_refresh_token, decode_token
from Ecommerce.app.exception.http import ConflictException, ResourceNotFoundException
from Ecommerce.app.models import UserRole
from Ecommerce.app.repository.RoleRepository import RoleRepository
from Ecommerce.app.repository.UserRepository import UserRepository
from Ecommerce.app.schemas.auth import RegisterRequest, RegisterResponse, LoginRequest, TokenResponse


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.db = db

    async def register(
            self,
            register_request: RegisterRequest,
            db: AsyncSession
    ) -> RegisterResponse:

        user_repo = UserRepository(db)
        role_repo = RoleRepository(db)

        existing_user = await user_repo.exists_by_user_name(register_request.user_name)
        if existing_user:
            raise ConflictException(f"User name '{register_request.user_name}' already exists'")

        user = to_user_entity(register_request)
        role = await role_repo.get_roles_by_codes(["USER"])
        if not role:
            raise ConflictException("Role not found")
        user.user_roles = [
            UserRole(role_id=role[0].id)
        ]

        await user_repo.save(user)
        return to_user_response(user)

    async def login(self, login_request: LoginRequest, db: AsyncSession) -> TokenResponse:
        user_repo = UserRepository(db)
        user = await user_repo.get_user_by_user_name(login_request.user_name)
        if not user:
            raise ResourceNotFoundException(f"User not found with user name '{login_request.user_name}'")

        if not verify_password(login_request.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password"
            )

        token_data = {
            "sub" : user.user_name,
            "user_name" : user.user_name,
            "full_name" : user.full_name,
            "roles": [ur.role.code for ur in user.user_roles]
        }
        access_token = create_access_token(data=token_data)
        refresh_token = create_refresh_token(data={"sub":user.user_name})
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    async def refresh_access_token(self, refresh_token: str, db: AsyncSession) -> TokenResponse:
        user_repo = UserRepository(db)
        payload = decode_token(refresh_token)
        if payload is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect refresh token")
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        user_name = payload.get("sub")
        if user_name is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        user = await user_repo.get_user_by_user_name(user_name)
        if not user:
            raise ResourceNotFoundException(f"User not found with user name '{user_name}'")

        token_data = {
            "sub": user.user_name,
            "user_name": user.user_name,
            "full_name": user.full_name,
            "roles": [ur.role.code for ur in user.user_roles]
        }

        access_token = create_access_token(data=token_data)
        new_refresh_token = create_refresh_token(data={"sub": user.user_name})

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token
        )





