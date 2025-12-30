from typing import Optional

from Ecommerce.app.builder.UserSearchBuilder import UserSearchBuilder
from Ecommerce.app.models import Role
from Ecommerce.app.models.User import User

from Ecommerce.app.schemas.user import UserResponse, UserSearchRequest

from Ecommerce.app.models.UserRole import UserRole
from Ecommerce.app.schemas.user import UserCreate

from Ecommerce.app.schemas.user import UserUpdate


class UserConverter:
    def to_user_response(self, user: User) -> UserResponse:
        return UserResponse(
            id=user.id,
            user_name=user.user_name,
            full_name=user.full_name,
            email=user.email,
            phone_number=user.phone_number,
            status=user.status,
            created_at=user.created_at,
            roles=[ur.role.code for ur in user.user_roles]
        )

    def create_user_to_entity(self, data: UserCreate, roles) -> User:
        user = User(
            user_name=data.user_name,
            full_name=data.full_name,
            email=data.email,
            phone_number=data.phone_number,
            status=data.status,
        )
        user_roles = []
        for role in roles:
            user_role = UserRole(role=role)
            user_roles.append(user_role)

        user.user_roles = user_roles
        return user

    def update_user_to_entity(self, user: User, data: UserUpdate, roles: Optional[list[Role]] = None) -> User:
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if field == "roles":
                continue
            else:
                setattr(user, field, value)

        if roles is not None:
            user.user_roles.clear()
            for role in roles:
                user_role = UserRole(role=role  )
                user.user_roles.append(user_role)  # Thêm vào danh sách user_roles của user

        return user

    def to_user_search_builder(self, request: UserSearchRequest) -> UserSearchBuilder:
        builder = UserSearchBuilder.Builder()
        builder.set_user_name(request.user_name)
        builder.set_full_name(request.full_name)
        builder.set_phone_number(request.phone_number)
        builder.set_email(request.email)
        builder.set_status(request.status)
        builder.set_roles(request.roles)
        return builder.build()