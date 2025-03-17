import uuid
from datetime import datetime

from pydantic import BaseModel


class NoteBaseSchema(BaseModel):
    title: str
    content: str


class NoteSchema(NoteBaseSchema):
    id: uuid.UUID


class NoteSchemaDetail(NoteSchema):
    created_at: datetime
    updated_at: datetime


class NoteCreateSchema(NoteBaseSchema):
    pass
