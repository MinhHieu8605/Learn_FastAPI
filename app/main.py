from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from Ecommerce.app.api.v1.router import router

from Ecommerce.app.exception.handlers import (
    resource_not_found_handler,
    validation_exception_handler,
    global_exception_handler
)
from Ecommerce.app.exception.http import ResourceNotFoundException

app = FastAPI(
    title="Ecommerce API",
    description="A simple ecommerce API",
    version="1.0.0",
)


origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(ResourceNotFoundException, resource_not_found_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

#include routers
app.include_router(router)

@app.get("/")
def read_root():
    return {"Hello": "World"}