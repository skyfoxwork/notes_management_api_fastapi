import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.ai import get_summarize_note_genai
from src.database.session_postgresql import get_db
from src.database.models.notes import Note


router = APIRouter()


@router.get("/{note_id}/")
async def get_note_summary(note_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    note = await db.get(Note, note_id)

    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    prompt = f"Summarize this note: {note.content}"
    response = await get_summarize_note_genai(prompt)

    return {"summary": response.text}
