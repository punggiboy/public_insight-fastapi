#테이블 선언 및 관계 설정

from database import Base 
from sqlalchemy import Column, Integer, String, ForeignKey

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index = True)
    email = Column(String(200))
    hashed_password = Column(String(512))


class Memo(Base):
    __tablename__ = "memo"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    title = Column(String(100))
    content = Column(String(200))