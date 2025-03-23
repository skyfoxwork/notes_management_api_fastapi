from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.session_postgresql import get_db
from src.database.models.notes import Note
from src.services.analytics import get_analyze_notes


router = APIRouter()


@router.get("/")
async def get_notes_analytics(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Note))
    notes = result.scalars().all()

    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    analyze_data = await get_analyze_notes(notes)

    return analyze_data
