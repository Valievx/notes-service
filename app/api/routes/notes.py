from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from schemas.note import NoteCreate, NoteUpdate, NoteRead
from services.note_service import NoteService
from repositories.note_repository import NoteRepository
from common.dependencies import get_current_user, get_current_admin
from models.user import User
from models.db_helper import get_session

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/", response_model=NoteRead)
async def create_note(
    note_in: NoteCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = NoteService(NoteRepository(session))
    return await service.create_note(current_user, note_in)


@router.get("/", response_model=List[NoteRead])
async def list_notes(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = NoteService(NoteRepository(session))
    return await service.list_notes(current_user)


@router.get("/{note_id}", response_model=NoteRead)
async def get_note(
    note_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = NoteService(NoteRepository(session))
    return await service.get_note(current_user, note_id)


@router.put("/{note_id}", response_model=NoteRead)
async def update_note(
    note_id: int,
    note_in: NoteUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = NoteService(NoteRepository(session))
    return await service.update_note(current_user, note_id, note_in)


@router.delete("/{note_id}")
async def delete_note(
    note_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = NoteService(NoteRepository(session))
    await service.delete_note(current_user, note_id)
    return {"detail": "Note deleted"}


@router.post("/{note_id}/restore")
async def restore_note(
    note_id: int,
    session: AsyncSession = Depends(get_session),
    current_admin: User = Depends(get_current_admin),
):
    service = NoteService(NoteRepository(session))
    await service.restore_note(current_admin, note_id)
    return {"detail": "Note restored"}


@router.get("/user/{user_id}", response_model=List[NoteRead])
async def get_user_notes(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_admin: User = Depends(get_current_admin),
):
    service = NoteService(NoteRepository(session))
    return await service.list_user_notes(current_admin, user_id)
