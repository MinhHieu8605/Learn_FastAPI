from fastapi import HTTPException


class ResourceNotFoundException(Exception):
    def __init__(self, message: str = "Resource not found"):
        self.message = message

class ConflictException(HTTPException):
    def __init__(self, message: str = "Conflict"):
        super().__init__(status_code=409, detail=message)
        self.message = message

class InsufficientStockException(Exception):
    def __init__(self, message: str = "Insufficient stock"):
        self.message = message