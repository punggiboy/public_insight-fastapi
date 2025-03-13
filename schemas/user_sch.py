# pydantic 라이브러리를 사용하여 데이터 검증을 위한 스키마를 정의(유효성 검증)
# 테이블마다 분리하여 정의

from pydantic import BaseModel
from typing import Optional

# 회원가입시 데이터 검증
class UserCreate(BaseModel):
    username: str 
    email: str 
    password: str #해쉬 전 패스워드를 받습니다.


# 회원로그인시 데이터 검증
class UserLogin(BaseModel):
    username: str 
    password: str 