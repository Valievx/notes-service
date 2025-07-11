from passlib.context import CryptContext

from repositories.user_repository import UserRepository
from models.user import User, Role
from schemas.user import UserCreate
from common.logging_config import get_logger

logger = get_logger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def authenticate_user(self, username: str, password: str) -> User | None:
        logger.info(f"Authenticating user: {username}")
        user = await self.user_repo.get_by_username(username)
        if not user:
            logger.warning(f"Authentication failed: User '{username}' not found")
            return None
        if not pwd_context.verify(password, user.hashed_password):
            logger.warning(f"Authentication failed: Incorrect password for user '{username}'")
            return None
        logger.info(f"User '{username}' authenticated successfully")
        return user

    async def register_user(self, user_create: UserCreate) -> User:
        logger.info(f"Registering new user: {user_create.username}")
        hashed_password = pwd_context.hash(user_create.password)
        user = User(
            username=user_create.username,
            hashed_password=hashed_password,
            role=Role.USER,
        )
        created_user = await self.user_repo.create(user)
        logger.info(f"User '{created_user.username}' registered successfully with id {created_user.id}")
        return created_user
