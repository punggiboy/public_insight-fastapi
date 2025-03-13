# 암호화, database session
from passlib.context import CryptContext

from database import AsyncSessionLocal 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # bcrypt 알고리즘을 사용하여 암호화

# 암호화
def get_password_hash(password):
    return pwd_context.hash(password)

# 암호화된 비밀번호와 비밀번호가 일치하는지 확인
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
        await session.commit()

# yield session은 세션을 요청 핸들러에게 제공
# session을 yield 하는 순간 FastAPI는 이를 의존성으로 주입
# yield 이후의 코드는 요청 핸들러의 실행이 끝난 후 실행
