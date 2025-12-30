from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str
    code: str   #ADMIN, STAFF, CUSTOMER

    class Config:
        from_attributes = True