from starlette.config import Config
from starlette.datastructures import Secret
config = Config(".env")

PROJECT_NAME: str = config("PROJECT_NAME", default="FastAPI example application")
DEBUG: bool = config("DEBUG", cast=bool, default=False)
VERSION: str = "0.0.0"
API_PREFIX: str = "/api"
SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)
JWT_TOKEN_PREFIX = "Token"

DATABASE_URL: str = config("DB_CONNECTION")
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)
