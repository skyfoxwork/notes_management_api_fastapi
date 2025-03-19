import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel


class NoteBaseSchema(BaseModel):
    title: str
    content: str


class NoteSchema(NoteBaseSchema):
    id: uuid.UUID


class VersionsSchema(BaseModel):
    id: uuid.UUID
    version: int
    content: str
    created_at: datetime


class NoteSchemaDetail(NoteSchema):
    created_at: datetime
    updated_at: datetime
    versions: List[VersionsSchema]


class NoteCreateSchema(NoteBaseSchema):
    pass


class NoteUpdateVersionCreateSchema(BaseModel):
    content: str
