from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserCreate
from repositories.user_repository import UserRepository
from services.user_service import UserService
from common.security import create_access_token
from models.db_helper import get_session
from models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register(user_in: UserCreate, session: AsyncSession = Depends(get_session)):
    user_repo = UserRepository(session)

    existing = await user_repo.get_by_username(user_in.username)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = pwd_context.hash(user_in.password)
    user = User(username=user_in.username, hashed_password=hashed_pw, role=user_in.role.value)
    session.add(user)
    await session.commit()
    return {"msg": f"User {user.username} created with role {user.role}"}


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user_repo = UserRepository(session)
    user_service = UserService(user_repo)
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
