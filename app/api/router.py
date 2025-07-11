from fastapi import APIRouter

from .routes import auth, notes

router = APIRouter()
router.include_router(auth.router)
router.include_router(notes.router)
