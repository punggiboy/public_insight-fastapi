# fastapi, session, database 처음 실행될 때 테이블 자동 생성, 

from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from database import engine, Base 
from fastapi.templating import Jinja2Templates
from controllers import router
from contextlib import asynccontextmanager





@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # 애플리케이션 시작 시 실행될 로직
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 애플리케이션 종료 시 실행될 로직

# FastAPI 애플리케이션 생성
# Swagger UI와 Redoc 비활성화
app = FastAPI(lifespan=app_lifespan, docs_url=None, redoc_url=None)
app.add_middleware(SessionMiddleware, secret_key="your-secret-key") #secret_key는 암호화 키로 임의로 설정




# router를 FastAPI 앱에 포함, router 등록
app.include_router(router)


templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
