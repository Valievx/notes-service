from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from models.user import User
from models.db_helper import get_session
from repositories.user_repository import UserRepository
from .settings import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_repo = UserRepository(session)
    user = await user_repo.get_by_username(username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_admin(user: User = Depends(get_current_user)):
    if user.role != "Admin":
        raise HTTPException(status_code=403, detail="Admin access only")
    return user
