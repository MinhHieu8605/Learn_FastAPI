from typing import Optional, List


class UserSearchBuilder:

    def __init__(self, builder: Builder):
        self.user_name = builder.user_name
        self.full_name = builder.full_name
        self.phone_number = builder.phone_number
        self.email = builder.email
        self.status = builder.status
        self.roles = builder.roles

    class Builder:
        def __init__(self):
            self.user_name: Optional[str] = None
            self.full_name: Optional[str] = None
            self.phone_number: Optional[str] = None
            self.email: Optional[str] = None
            self.status: Optional[int] = None
            self.roles: Optional[List[str]] = None

        def set_user_name(self, user_name: str) -> UserSearchBuilder.Builder:
            self.user_name = user_name
            return self

        def set_full_name(self, full_name: str) -> UserSearchBuilder.Builder:
            self.full_name = full_name
            return self

        def set_phone_number(self, phone_number: str) -> UserSearchBuilder.Builder:
            self.phone_number = phone_number
            return self

        def set_email(self, email: str) -> UserSearchBuilder.Builder:
            self.email = email
            return self

        def set_status(self, status: int) -> UserSearchBuilder.Builder:
            self.status = status
            return self

        def set_roles(self, roles) -> UserSearchBuilder.Builder:
            if roles is None:
                self.roles = None
            elif isinstance(roles, str):
                self.roles = [r.strip() for r in roles.split(",")]
            else:
                self.roles = list(roles)
            return self

        def build(self) -> UserSearchBuilder:
            return UserSearchBuilder(self)
