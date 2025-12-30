from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "Pending",
    CONFIRMED = "Confirmed",
    PROCESSING = "Processing",
    SHIPPED = "Shipped",
    CANCELLED = "Cancelled"
    RETURNED = "Returned"