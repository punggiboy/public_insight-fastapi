# pydantic 라이브러리를 사용하여 데이터 검증을 위한 스키마를 정의(유효성 검증)
# 테이블마다 분리하여 정의
import sys, os 
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from pydantic import BaseModel
from typing import Optional


class MemoCreate(BaseModel):
    title: str 
    content: str 

class MemoUpdate(BaseModel):
    title: Optional[str] = None 
    content: Optional[str] = None 