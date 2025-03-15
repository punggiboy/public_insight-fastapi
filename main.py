# fastapi, session, database 처음 실행될 때 테이블 자동 생성하는 파일

import os
from dotenv import load_dotenv
import time

from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.exc import OperationalError

from database import engine, Base 
from controllers import router
from contextlib import asynccontextmanager


# 애플리케이션 시작 시 테이블을 자동으로 생성하는 로직
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

# 환경 변수 로드
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

# 세션 미들웨어 추가
app.add_middleware(SessionMiddleware, secret_key="SECRET_KEY") #secret_key는 암호화 키로 임의로 설정

# MySQL 데이터베이스가 준비되기 전에 잠시 대기하는 코드
# Docker에서 MySQL이 올라가자마자 연결되도록 시간 간격을 두고 재시도
retries = 5
while retries > 0:
    try:
        conn = engine.connect()
        Base.metadata.create_all(bind=engine)
        break
    except OperationalError:
        retries -= 1
        print(f"Database connection failed. Retries left: {retries}")
        time.sleep(5)

if retries == 0:
    raise Exception("Could not connect to the database")

    
# FastAPI 앱에 router 등록
# `router`는 controllers.py에서 정의된 라우터로, 이를 FastAPI 앱에 등록하여 API 엔드포인트를 활성화합니다.
app.include_router(router)

@app.get("/")
def read_root():
    return {"Hello": "World"}