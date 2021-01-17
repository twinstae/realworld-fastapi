# realworld-fastapi
https://github.com/nsidnev/fastapi-realworld-example-app 의 실습

## Django Rest Framework 와 비교
Starllette : FastAPI가 의존하는 ASGI 서버 프레임워크
Uvicorn : Starllette이 의존하는 ASGI 서버 프레임워크

### views.py

### urls.py, router
[APIRouter](https://fastapi.tiangolo.com/ko/tutorial/bigger-applications/?h=+include#include-an-apirouter-in-another)를 지원한다.

### exception_handler
[exception_handler](https://fastapi.tiangolo.com/ko/tutorial/handling-errors/) 를 지원한다.

### serializer, renderer
Pydantic : json parse, dump 

### ORM, models.py
Aiosqlite : async SQLite3 SQL DB connection
Asyncpg : async Postegral SQL DB connection
Asyncio : 위 두 프레임워크가 의존하는 async highlevel api
SQLAlchemy : ORM, 모델 정의
Databases : Async ORM for SQLAlchemy
Alembic : lightweight DB migration for SQLAlchemy

### Auth
Bcrypt : password hash
PyJwt : Json Web Token 보안 제공

### APIClient for Test
requests : TestClient 를 제공

### 그 외 기타
slugify : title등을 slug로 변환
