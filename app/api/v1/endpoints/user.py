from typing import List, Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from Ecommerce.app.api.deps import require_roles
from Ecommerce.app.constant.SystemConstant import SystemConstant
from Ecommerce.app.core.deps import get_db
from Ecommerce.app.repository.UserRepository import UserRepository
from Ecommerce.app.schemas.user import UserResponse, UserCreate, UserSearchRequest
from Ecommerce.app.services.UserService import UserService

from Ecommerce.app.repository.RoleRepository import RoleRepository

from Ecommerce.app.schemas.user import UserUpdate

router = APIRouter()

@router.post("/search", response_model=List[UserResponse])
async def get_all_users(
    search_request: UserSearchRequest,
    current_user=Depends(require_roles([SystemConstant.ADMIN_ROLE])),
    db: AsyncSession = Depends(get_db)
):
    service = UserService(UserRepository(db), RoleRepository(db))
    result = await service.get_all_users(search_request)
    return result

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new user",
    response_description="User created successfully"
)
async def create_user(
    user_data: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user=Depends(require_roles([SystemConstant.ADMIN_ROLE]))
):
    service = UserService(
        UserRepository(db),
        RoleRepository(db)
    )
    return await service.create_user(user_data)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user : UserUpdate,
    current_user=Depends(require_roles([SystemConstant.ADMIN_ROLE])),
    db: AsyncSession = Depends(get_db)
):
    service = UserService(UserRepository(db), RoleRepository(db))
    return await service.update_user(user, user_id)

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    current_user=Depends(require_roles([SystemConstant.ADMIN_ROLE])),
    db: AsyncSession = Depends(get_db)
):
    service = UserService(UserRepository(db), RoleRepository(db))
    await service.delete_user(user_id)
    return {"message": "User has been successfully deleted (soft delete)."}

@router.put("/password/{user_id}/reset", status_code=status.HTTP_200_OK)
async def reset_password(
    user_id: int,
    current_user=Depends(require_roles([SystemConstant.ADMIN_ROLE])),
    db: AsyncSession = Depends(get_db)
):
    service = UserService(UserRepository(db), RoleRepository(db))
    await service.reset_password(user_id)
    return {"message": "Password has been successfully reset."}

