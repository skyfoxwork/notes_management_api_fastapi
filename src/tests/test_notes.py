import uuid

import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.accounts import (
    UserModel,
    UserGroupModel,
    UserGroupEnum
)
from src.database.models.notes import Note, NoteVersion
from src.security.token_manager import JWTAuthManager
from src.tests.utils import create_user, generate_token



def generate_token(user_id, jwt_manager):
    """
    Generates an access token for a user.
    """
    return jwt_manager.create_access_token({"user_id": user_id})


async def create_user(db_session: AsyncSession):
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

    return user


@pytest.mark.asyncio
async def test_empty_note(
        client: AsyncClient,
        db_session: AsyncSession,
        jwt_manager: JWTAuthManager
):
    user = await create_user(db_session)

    token = generate_token(user.id, jwt_manager)
    response = await client.get(
        "/api/v1/notes/", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "No notes found."}


@pytest.mark.asyncio
async def test_create_and_read_note(
        client: AsyncClient,
        db_session: AsyncSession,
        jwt_manager: JWTAuthManager
):
    user = await create_user(db_session)

    note = Note(
        title="Test Note", content="This is a test note", user_id=user.id
    )
    db_session.add(note)

    await db_session.commit()
    await db_session.refresh(note)

    token = generate_token(user.id, jwt_manager)
    response = await client.get(
        "/api/v1/notes/", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json() == [
        {"id": str(note.id), "title": note.title, "content": note.content}
    ]


######


@pytest.mark.asyncio
async def test_get_note_by_id(
        client: AsyncClient,
        db_session: AsyncSession,
        jwt_manager: JWTAuthManager
):
    user = await create_user(db_session)

    note = Note(
        title="Test Note",
        content="This is a test note",
        user_id=user.id
    )
    db_session.add(note)

    await db_session.commit()
    await db_session.refresh(note)

    token = generate_token(user.id, jwt_manager)
    response = await client.get(
        f"/api/v1/notes/{note.id}/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": str(note.id),
        "title": note.title,
        "content": note.content,
        "updated_at": note.updated_at.isoformat(),
        "created_at": note.created_at.isoformat(),
        "versions": []
    }


@pytest.mark.asyncio
async def test_delete_note(
        client: AsyncClient,
        db_session: AsyncSession,
        jwt_manager: JWTAuthManager
):
    user = await create_user(db_session)

    note = Note(
        title="Test Note", content="This is a test note", user_id=user.id
    )
    db_session.add(note)

    await db_session.commit()
    await db_session.refresh(note)

    token = generate_token(user.id, jwt_manager)

    response = await client.delete(
        f"/api/v1/notes/{note.id}/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204

    db_session.expunge(note)

    db_note = await db_session.get(Note, note.id)

    assert db_note is None


@pytest.mark.asyncio
async def test_delete_non_existing_note(
        client: AsyncClient,
        db_session: AsyncSession,
        jwt_manager: JWTAuthManager
):
    user = await create_user(db_session)

    token = generate_token(user.id, jwt_manager)

    response = await client.delete(
        f"/api/v1/notes/{uuid.uuid4()}/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Note with the given UUID was not found."
    }


@pytest.mark.asyncio
async def test_update_note(
        client: AsyncClient,
        db_session: AsyncSession,
        jwt_manager: JWTAuthManager
):
    user = await create_user(db_session)

    note = Note(
        title="Test Note", content="This is a test note", user_id=user.id
    )
    db_session.add(note)
    await db_session.commit()
    await db_session.refresh(note)

    token = generate_token(user.id, jwt_manager)

    new_content = "Updated content"
    response = await client.patch(
        f"/api/v1/notes/{note.id}/",
        json={"content": new_content},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["content"] == new_content

    updated_note = await db_session.get(Note, note.id)
    await db_session.refresh(updated_note)
    assert updated_note.content == new_content
