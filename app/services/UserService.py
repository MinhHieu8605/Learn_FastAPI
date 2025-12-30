from typing import List, Optional

from Ecommerce.app.constant.SystemConstant import SystemConstant
from Ecommerce.app.converter.UserConverter import UserConverter
from Ecommerce.app.core.security import get_password_hash
from Ecommerce.app.exception.http import ResourceNotFoundException, ConflictException
from Ecommerce.app.repository.RoleRepository import RoleRepository
from Ecommerce.app.repository.UserRepository import UserRepository
from Ecommerce.app.schemas.user import UserCreate, UserResponse, UserSearchRequest

from Ecommerce.app.schemas.user import UserUpdate



class UserService:
    def __init__(self,
        user_repo: Optional[UserRepository] = None,
        role_repo: Optional[RoleRepository] = None
    ):
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.user_converter = UserConverter()

    async def get_all_users(self, search_request: UserSearchRequest) -> list[UserResponse]:
        user_search_builder = self.user_converter.to_user_search_builder(search_request)

        users = await self.user_repo.get_users(user_search_builder)
        user_response_list: List[UserResponse] = []
        for item in users:
            user_response = self.user_converter.to_user_response(item)
            user_response_list.append(user_response)

        return user_response_list

    async def create_user(self, data: UserCreate) -> UserResponse:
        existing_user = await self.user_repo.get_user_by_user_name(data.user_name)
        if existing_user:
            raise ConflictException(f"User name '{data.user_name}' already exists'")

        roles = await self.role_repo.get_roles_by_codes(data.roles)
        if not roles:
            raise ResourceNotFoundException(f"Role '{data.roles}' not found")

        data.password = get_password_hash(data.password)
        user = self.user_converter.create_user_to_entity(data, roles)

        await self.user_repo.save(user)
        return self.user_converter.to_user_response(user)


    async def update_user(self, data: UserUpdate, user_id: int) -> UserResponse:
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise ResourceNotFoundException(f"User with id '{user_id}' not found")

        update_data = data.model_dump(exclude_unset=True)

        if "user_name" in update_data and update_data["user_name"] != user.user_name:
            existing_user_name = await self.user_repo.get_user_by_user_name(update_data["user_name"])
            if existing_user_name:
                raise ConflictException(f"User name '{update_data['user name']}' already exists'")
        if "password" in update_data:
            update_data["password"] = get_password_hash(update_data["password"])

        roles = None
        if "roles" in update_data:
            roles = await self.role_repo.get_roles_by_codes(update_data["roles"])
            if not roles:
                raise ResourceNotFoundException("Role not found")
        user = self.user_converter.update_user_to_entity(user, data, roles)

        await self.user_repo.save(user)
        return self.user_converter.to_user_response(user)

    async def delete_user(self, user_id: int) -> None:
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise ResourceNotFoundException(f"User not found with id = {user_id}")
        user.status = 0
        await self.user_repo.save(user)

    async def reset_password(self, user_id: int):
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise ResourceNotFoundException(f"User not found with id = {user_id}")
        user.password = get_password_hash(SystemConstant.DEFAULT_PASSWORD)
        await self.user_repo.save(user)
        return user




