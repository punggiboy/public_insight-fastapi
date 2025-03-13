# Description: This file contains the controllers for the API endpoints

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
templates = Jinja2Templates(directory="templates") 


# 회원가입
@router.post("/signup")
async def signup(signup_data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == signup_data.username))
    
    # 이미 존재하는 사용자인지 확인
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = get_password_hash(signup_data.password)
    new_user = User(username=signup_data.username, email=signup_data.email, hashed_password=hashed_password)
    
    db.add(new_user)
    try:
        await db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="회원가입 실패, 가입한 내용 확인")

    await db.refresh(new_user)
    return {"message":"회원가입 성공"}


# 로그인
@router.post("/login")
async def login(request: Request, signin_data: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == signin_data.username))

    user = result.scalars().first()
    if user and verify_password(signin_data.password, user.hashed_password):
        request.session["username"] = user.username 
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid crendentials")


# 로그아웃
@router.post("/logout")
async def logout(requset: Request):
    requset.session.pop("username", None) #세션에서 username을 제거, 세션관리
    return {"message": "Logout successful"}


# 메모 생성
@router.post("/memos/")
async def create_memo(request: Request, memo: MemoCreate, db: AsyncSession = Depends(get_db)):
    username = request.session.get("username")
    if username is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first() 

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_memo = Memo(user_id=user.id, title= memo.title, content=memo.content)
    db.add(new_memo)
    await db.commit()
    await db.refresh(new_memo)
    return new_memo


# 메모 조회
@router.get("/memos/")
async def list_memo(request: Request, db: Session = Depends(get_db)):
    username = request.session.get("username")
    if username is None: 
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first() 

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    memos = await db.execute(select(Memo).where(Memo.user_id == user.id))
    memos = memos.scalars().all()
    return templates.TemplateResponse("memos.html", {"request": request, "memos": memos})


# 메모 수정
@router.put("/memos/{memo_id}")
async def update_memo(request: Request, memo_id: int, memo: MemoUpdate, db: Session = Depends(get_db)):
    username = request.session.get("username")
    if username is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first() 

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = await db.execute(select(Memo).where(Memo.user_id == user.id, Memo.id == memo_id))
    db_memo = result.scalars().first()
    if db_memo is None:
        return {"error": "Memo not found"}
    
    if memo.title is not None:
        db_memo.title = memo.title
    if memo.content is not None: 
        db_memo.content = memo.content 
    
    await db.commit()
    await db.refresh(db_memo)
    return db_memo


# 메모 삭제
@router.delete("/memos/{memo_id}")
async def delete_memo(request: Request, memo_id: int, db: Session = Depends(get_db)):
    username = request.session.get("username")
    if username is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first() 

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = await db.execute(select(Memo).where(Memo.user_id == user.id, Memo.id == memo_id))
    db_memo = result.scalars().first()
    if db_memo is None:
        return ({"error": "Memo not found"})
    
    await db.delete(db_memo)
    await db.commit()
    return ({"message": "Memo deleted successfully"})


# 기존 라우터
@router.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/about")
async def about():
    return {"message": "이것은 마이 메모 앱의 소개 페이지입니다."}