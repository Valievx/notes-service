from typing import List

from fastapi import HTTPException

from models.note import Note
from models.user import User, Role
from schemas.note import NoteCreate, NoteUpdate
from repositories.note_repository import NoteRepository
from common.logging_config import get_logger

logger = get_logger(__name__)


class NoteService:
    def __init__(self, note_repo: NoteRepository):
        self.note_repo = note_repo

    async def create_note(self, user: User, note_in: NoteCreate) -> Note:
        note = Note(**note_in.dict(), owner_id=user.id)
        created_note = await self.note_repo.create(note)
        logger.info(f"Note {created_note.id} created by user {user.id}")
        return created_note

    async def get_note(self, user: User, note_id: int) -> Note:
        note = await self.note_repo.get_by_id(note_id)
        if not note or (note.is_deleted and user.role != Role.ADMIN):
            logger.warning(f"Note {note_id} not found or deleted for user {user.id}")
            raise HTTPException(status_code=404, detail="Note not found")

        if user.role == Role.ADMIN or note.owner_id == user.id:
            return note
        logger.warning(f"User {user.id} unauthorized to access note {note_id}")
        raise HTTPException(status_code=403, detail="Access denied")

    async def list_notes(self, user: User) -> List[Note]:
        if user.role == Role.ADMIN:
            return await self.note_repo.list_all()
        return await self.note_repo.list_by_owner(user.id)

    async def update_note(self, user: User, note_id: int, note_in: NoteUpdate) -> Note:
        note = await self.get_note(user, note_id)
        if user.role != Role.ADMIN and note.owner_id != user.id:
            logger.warning(f"User {user.id} unauthorized to update note {note_id}")
            raise HTTPException(status_code=403, detail="Access denied")

        for field, value in note_in.dict(exclude_unset=True).items():
            setattr(note, field, value)

        updated_note = await self.note_repo.update(note)
        logger.info(f"Note {note_id} updated by user {user.id}")
        return updated_note

    async def delete_note(self, user: User, note_id: int):
        note = await self.get_note(user, note_id)
        if user.role != Role.ADMIN and note.owner_id != user.id:
            logger.warning(f"User {user.id} unauthorized to delete note {note_id}")
            raise HTTPException(status_code=403, detail="Access denied")
        await self.note_repo.soft_delete(note)
        logger.info(f"Note {note_id} deleted by user {user.id}")

    async def restore_note(self, admin_user: User, note_id: int):
        if admin_user.role != Role.ADMIN:
            logger.warning(
                f"User {admin_user.id} attempted to "
                f"restore note {note_id} without permission"
            )
            raise HTTPException(status_code=403, detail="Admins only")
        note = await self.note_repo.get_by_id(note_id)
        if not note or not note.is_deleted:
            logger.warning(f"Note {note_id} not found or not deleted for restore")
            raise HTTPException(status_code=404, detail="Note not found or not deleted")
        await self.note_repo.restore(note)
        logger.info(f"Note {note_id} restored by admin {admin_user.id}")

    async def list_user_notes(self, admin_user: User, user_id: int):
        logger.info(f"Admin {admin_user.id} is listing notes for user {user_id}")
        if admin_user.role != Role.ADMIN:
            logger.warning(
                f"User {admin_user.id} attempted to "
                f"list notes for user {user_id} without permission"
            )
            raise HTTPException(status_code=403, detail="Admins only")
        return await self.note_repo.list_by_owner(user_id)
