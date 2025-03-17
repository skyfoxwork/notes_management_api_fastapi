import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.session_postgresql import get_db
from src.database.models.notes import Note
from src.schemas.notes import NoteCreateSchema, NoteSchema, NoteSchemaDetail


router = APIRouter()


@router.get("/", response_model=list[NoteSchema], status_code=status.HTTP_200_OK)
async def get_list_of_notes(db: AsyncSession = Depends(get_db)):
    db_result = await db.execute(select(Note))
    notes = db_result.scalars().all()

    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No notes found.")

    return notes


@router.get("/{note_id}/", response_model=NoteSchemaDetail, status_code=status.HTTP_200_OK)
async def get_note_by_id(note_id: uuid.UUID , db: AsyncSession = Depends(get_db)):
    db_result = await db.execute(select(Note).filter(Note.id == note_id))
    note = db_result.scalar_one_or_none()

    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return note


@router.post("/", response_model=NoteSchema, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteCreateSchema, db: AsyncSession = Depends(get_db)):
    new_note = Note(title=note.title, content=note.content)
    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    return new_note
