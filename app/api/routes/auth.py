from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserCreate, UserRead
from repositories.user_repository import UserRepository
from services.user_service import UserService
from common.security import create_access_token
from models.db_helper import get_session

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserRead)
async def register(user_create: UserCreate, session: AsyncSession = Depends(get_session)):
    user_repo = UserRepository(session)
    user_service = UserService(user_repo)
    existing_user = await user_repo.get_by_username(user_create.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user = await user_service.register_user(user_create)
    return user


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
