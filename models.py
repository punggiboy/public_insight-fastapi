#테이블 선언 및 관계 설정하는 파일

from database import Base 
from sqlalchemy import Column, Integer, String, ForeignKey


class Memo(Base):
    __tablename__ = "memo"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    title = Column(String(100))
    content = Column(String(200))