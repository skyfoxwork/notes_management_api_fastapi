import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.functions import coalesce

from src.database.session_postgresql import get_db
from src.database.models.notes import Note, NoteVersion
from src.schemas.notes import NoteCreateSchema, NoteSchema, NoteSchemaDetail, NoteUpdateCreateVersionSchema


router = APIRouter()


@router.get("/", response_model=list[NoteSchema], status_code=status.HTTP_200_OK)
async def get_list_of_notes(db: AsyncSession = Depends(get_db)):
    db_result = await db.execute(select(Note))
    notes = db_result.scalars().all()

    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No notes found.")

    return notes


@router.get("/{note_id}/", response_model=NoteSchemaDetail, status_code=status.HTTP_200_OK)
async def get_note_by_id(note_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    db_result = await db.execute(
        select(Note)
        .options(selectinload(Note.versions))
        .filter(Note.id == note_id)
    )
    note = db_result.scalars().first()

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


@router.delete("/{note_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(delete(Note).where(Note.id == note_id))
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note with the given UUID was not found."
        )
    await db.commit()


@router.patch("/{note_id}/", response_model=NoteSchema, status_code=status.HTTP_200_OK)
async def update_note(data: NoteUpdateCreateVersionSchema, note_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    note = await db.get(Note, note_id)

    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if note.content == data.content:
        return {"detail": "content not changed"}

    version_number = (await db.execute(
        select(coalesce(func.max(NoteVersion.version), 0))
        .filter(NoteVersion.note_id == note_id)
    )).scalar()

    new_version = NoteVersion(
        note_id=note.id,
        version=version_number + 1,
        content=note.content
    )

    db.add(new_version)

    note.content = data.content

    await db.commit()
    await db.refresh(note)

    return note
