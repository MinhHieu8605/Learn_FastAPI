from typing import Annotated

from fastapi import APIRouter,status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Ecommerce.app.api.deps import require_roles
from Ecommerce.app.constant.SystemConstant import SystemConstant
from Ecommerce.app.core.deps import get_db
from Ecommerce.app.schemas.auth import RegisterResponse, RegisterRequest, TokenResponse, LoginRequest, \
    RefreshTokenRequest
from Ecommerce.app.services.AuthService import AuthService

router = APIRouter()

@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register account",
    response_description="User created successfully"
)
async def register(
    user_data: RegisterRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    service = AuthService(db)
    return await service.register(user_data, db)

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Login user",
    response_description="User logged in"
)
async def login(
    user_data: LoginRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    service = AuthService(db)
    return await service.login(user_data, db)

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles([SystemConstant.ADMIN_ROLE]))
):
    auth_service = AuthService(db)
    return await auth_service.refresh_access_token(refresh_request.refresh_token, db)