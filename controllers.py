# 이 파일은 API 엔드포인트의 컨트롤러를 정의하는 파일
# 각 엔드포인트에서 요청을 처리하고, 적절한 응답을 반환하는 역할

from fastapi import APIRouter 
from fastapi.templating import Jinja2Templates
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select 

from models import User, Memo
from schemas.memo_sch import MemoCreate, MemoUpdate
from schemas.user_sch import UserCreate, UserLogin
from dependencies import get_password_hash, verify_password, get_db

router = APIRouter()