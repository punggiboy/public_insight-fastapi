# 데이터베이스 접속, 세션 생성, Base 선언, 

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DATABASE_URL = "mysql+aiomysql://bee:bee2001@localhost/my_memo_app"
engine = create_async_engine(DATABASE_URL, echo=True)
# echo=True는 SQL문을 출력하도록 설정

AsyncSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine,
    class_=AsyncSession)

Base = declarative_base()