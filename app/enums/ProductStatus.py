from enum import Enum
class ProductStatus(str,Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    OUT_OF_STOCK = "OUT_OF_STOCK"
    BLOCKED = "BLOCKED"
    DELETED = "DELETED"