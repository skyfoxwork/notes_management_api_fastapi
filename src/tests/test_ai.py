import uuid

import pytest
from unittest.mock import AsyncMock

from src.database.models.notes import Note


@pytest.mark.asyncio
async def test_get_note_summary(client, mocker, db_session):
    """
    The test to get a note summary with mocking an external API.
    """

    note = Note(title="Test title", content="Test content")
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
async def test_get_note_summary_not_found(client, mocker):
    """The test to get an error if a note is not found."""

    # Request with invalid ID
    note_id = uuid.uuid4()
    response = await client.get(f"/api/v1/summarize/{note_id}/")

    assert response.status_code == 404
    assert response.json() == {"detail": "Not found."}
