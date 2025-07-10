from typing import Optional

from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    title: str = Field(..., max_length=256)
    body: str = Field(..., max_length=65536)


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=256)
    body: Optional[str] = Field(None, max_length=65536)


class NoteRead(NoteBase):
    id: int
    is_deleted: bool
    owner_id: int

    class Config:
        orm_mode = True
