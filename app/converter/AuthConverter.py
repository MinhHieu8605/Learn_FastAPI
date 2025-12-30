from Ecommerce.app.core.security import get_password_hash
from Ecommerce.app.models import User
from Ecommerce.app.schemas.auth import RegisterRequest, RegisterResponse


def to_user_entity(data: RegisterRequest) -> User:
    user = User(
        user_name=data.user_name,
        full_name=data.full_name,
        email=data.email,
        password=get_password_hash(data.password),
        phone_number=data.phone_number,
        status=data.status,
    )
    return user

def to_user_response(data: User) -> RegisterResponse:
    user = User(
        id=data.id,
        user_name=data.user_name,
        full_name=data.full_name,
        email=data.email,
        phone_number=data.phone_number,
        status=data.status,
    )
    return user