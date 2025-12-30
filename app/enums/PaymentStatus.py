from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "Pending",
    COMPLETED = "Completed",
    FAILED = "Failed",
    RETURNED = "Returned"