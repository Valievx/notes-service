from typing import List

from fastapi import HTTPException

from models.note import Note
from models.user import User, Role
from schemas.note import NoteCreate, NoteUpdate
from repositories.note_repository import NoteRepository


class NoteService:
    def __init__(self, note_repo: NoteRepository):
        self.note_repo = note_repo

    async def create_note(self, user: User, note_in: NoteCreate) -> Note:
        note = Note(**note_in.dict(), owner_id=user.id)
        return await self.note_repo.create(note)

    async def get_note(self, user: User, note_id: int) -> Note:
        note = await self.note_repo.get_by_id(note_id)
        if not note or (note.is_deleted and user.role != Role.ADMIN):
            raise HTTPException(status_code=404, detail="Note not found")

        if user.role == Role.ADMIN or note.owner_id == user.id:
            return note
        raise HTTPException(status_code=403, detail="Access denied")

    async def list_notes(self, user: User) -> List[Note]:
        if user.role == Role.ADMIN:
            return await self.note_repo.list_all()
        return await self.note_repo.list_by_owner(user.id)

    async def update_note(self, user: User, note_id: int, note_in: NoteUpdate) -> Note:
        note = await self.get_note(user, note_id)
        if user.role != Role.ADMIN and note.owner_id != user.id:
            raise HTTPException(status_code=403, detail="Access denied")

        for field, value in note_in.dict(exclude_unset=True).items():
            setattr(note, field, value)

        return await self.note_repo.update(note)

    async def delete_note(self, user: User, note_id: int):
        note = await self.get_note(user, note_id)
        if user.role != Role.ADMIN and note.owner_id != user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        await self.note_repo.soft_delete(note)

    async def restore_note(self, admin_user: User, note_id: int):
        if admin_user.role != Role.ADMIN:
            raise HTTPException(status_code=403, detail="Admins only")
        note = await self.note_repo.get_by_id(note_id)
        if not note or not note.is_deleted:
            raise HTTPException(status_code=404, detail="Note not found or not deleted")
        await self.note_repo.restore(note)

    async def list_user_notes(self, admin_user: User, user_id: int):
        if admin_user.role != Role.ADMIN:
            raise HTTPException(status_code=403, detail="Admins only")
        return await self.note_repo.list_by_owner(user_id)
