import pytest

from src.database.models.notes import Note


@pytest.mark.asyncio
async def test_empty_note(client):
    response = await client.get("/api/v1/notes/")
    assert response.status_code == 404
    assert response.json() == {"detail": "No notes found."}


@pytest.mark.asyncio
async def test_create_and_read_note(client, db_session):
    note = Note(title="Test Note", content="This is a test note")
    db_session.add(note)
    await db_session.commit()
    await db_session.refresh(note)

    response = await client.get("/api/v1/notes/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json() == [{"id": str(note.id), "title": note.title, "content": note.content}]


@pytest.mark.asyncio
async def test_create_and_read_note_second(client, db_session):
    note = Note(title="Test", content="This")
    db_session.add(note)
    await db_session.commit()
    await db_session.refresh(note)

    response = await client.get("/api/v1/notes/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json() == [{"id": str(note.id), "title": note.title, "content": note.content}]
