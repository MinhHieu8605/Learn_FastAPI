from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Ecommerce API"
    SQLALCHEMY_DATABASE_ECOMMERCE_URI: str = "postgresql+asyncpg://postgres:123456@localhost:5432/Ecommerce"

    class Config:
        env_file = ".env"

    # jwt settings
    SECRET_KEY: str = "VYx8FJpFfH4z9qN9mZr9W0yYx7Q3kYwB1xMZkM6Zk8Q"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    #security
    BCRYPT_ROUNDS: int = 12
settings = Settings()