from passlib.context import CryptContext

from repositories.user_repository import UserRepository
from models.user import User, Role
from schemas.user import UserCreate


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def authenticate_user(self, username: str, password: str) -> User | None:
        user = await self.user_repo.get_by_username(username)
        if not user:
            return None
        if not pwd_context.verify(password, user.hashed_password):
            return None
        return user

    async def register_user(self, user_create: UserCreate) -> User:
        hashed_password = pwd_context.hash(user_create.password)
        user = User(
            username=user_create.username,
            hashed_password=hashed_password,
            role=Role.USER,
        )
        return await self.user_repo.create(user)
