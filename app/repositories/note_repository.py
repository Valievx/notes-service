from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.note import Note


class NoteRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, note: Note) -> Note:
        self.session.add(note)
        await self.session.commit()
        await self.session.refresh(note)
        return note

    async def get_by_id(self, note_id: int) -> Note | None:
        stmt = select(Note).where(Note.id == note_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_owner(self, owner_id: int) -> list[Note]:
        stmt = select(Note).where(Note.owner_id == owner_id, Note.is_deleted == False)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def list_all(self) -> list[Note]:
        stmt = select(Note)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, note: Note) -> Note:
        self.session.add(note)
        await self.session.commit()
        await self.session.refresh(note)
        return note

    async def soft_delete(self, note: Note):
        note.is_deleted = True
        await self.update(note)

    async def restore(self, note: Note):
        note.is_deleted = False
        await self.update(note)
