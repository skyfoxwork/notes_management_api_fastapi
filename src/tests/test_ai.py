import uuid

import pytest
from unittest.mock import AsyncMock
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.notes import Note
from src.database.models.accounts import UserModel, UserGroupModel,UserGroupEnum


@pytest.mark.asyncio
async def test_get_note_summary(client: AsyncClient , mocker, db_session: AsyncSession):
    """
    The test to get a note summary with mocking an external API.
    """
    user_group = UserGroupModel(name=UserGroupEnum.USER)
    db_session.add(user_group)

    await db_session.commit()
    await db_session.refresh(user_group)

    user = UserModel.create(
        email="test@test.com",
        raw_password="Test_password12345@",
        group_id=user_group.id,
    )

    db_session.add(user)

    await db_session.commit()
    await db_session.refresh(user)

    note = Note(title="Test title", content="Test content", user_id=user.id)
    db_session.add(note)

    await db_session.commit()
    await db_session.refresh(note)

    # Moke to response from the AI service
    mock_response = AsyncMock()
    mock_response.text = "This is a summarized note."

    # Mock get_summarize_note_genai function
    mocker.patch("src.routes.ai.get_summarize_note_genai", return_value=mock_response)

    response = await client.get(f"/api/v1/summarize/{note.id}/")

    assert response.status_code == 200
    assert response.json() == {"id": str(note.id), "summary": "This is a summarized note."}


@pytest.mark.asyncio
async def test_get_note_summary_not_found(client: AsyncClient, mocker):
    """The test to get an error if a note is not found."""

    # Request with invalid ID
    note_id = uuid.uuid4()
    response = await client.get(f"/api/v1/summarize/{note_id}/")

    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}
