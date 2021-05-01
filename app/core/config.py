from starlette.config import Config
from starlette.datastructures import Secret
config = Config(".env")

PROJECT_NAME: str = config("PROJECT_NAME", default="FastAPI example application")
DEBUG: bool = config("DEBUG", cast=bool, default=False)
VERSION: str = "0.0.0"
API_PREFIX: str = "/api"
SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret, default="t4e1s3t2i8n7g")
JWT_TOKEN_PREFIX = "Token"

IS_TEST = True
DATABASE_URL: str = config("DB_CONNECTION", default="sqlite://test.db")
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)
