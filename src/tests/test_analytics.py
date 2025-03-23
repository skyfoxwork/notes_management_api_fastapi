import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.notes import Note
from src.security.token_manager import JWTAuthManager
from src.tests.utils import create_user, generate_token


@pytest.mark.asyncio
async def test_get_notes_analytics_success(
        client: AsyncClient,
        db_session: AsyncSession,
        jwt_manager: JWTAuthManager
):
    """
    Test the success scenario when notes are present and analytics are generated correctly.
    """

    user = await create_user(db_session)

    note_1 = Note(title="Test Note 1", content="Content of note 1", user_id=user.id)
    note_2 = Note(title="Test Note 2", content="Content of note 2", user_id=user.id)

    db_session.add(note_1)
    db_session.add(note_2)

    await db_session.commit()

    token = generate_token(user.id, jwt_manager)

    response = await client.get("/api/v1/analytics/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    response_data = response.json()

    expected_structure = {
        'total_word_count': int,
        'average_note_length': float,
        'most_common_words': list,
        'top_3_longest_notes': list,
        'top_3_shortest_notes': list
    }

    for key, expected_type in expected_structure.items():
        assert key in response_data, f"Key {key} is missing in the response"
        assert isinstance(
            response_data[key], expected_type
        ), f"Key {key} should be of type {expected_type}"

    assert isinstance(response_data["most_common_words"], list)
    assert (
        all(isinstance(word_pair, list) and
            len(word_pair) == 2 for word_pair in response_data["most_common_words"])
    )
    assert isinstance(response_data["top_3_longest_notes"], list)
    assert (
        all(isinstance(note, dict) and
            "id" in note and "word_count" in
            note for note in response_data["top_3_longest_notes"])
    )
    assert isinstance(response_data["top_3_shortest_notes"], list)
    assert (
        all(isinstance(note, dict) and
            "id" in note and "word_count" in
            note for note in response_data["top_3_shortest_notes"])
    )

    assert len(response_data) > 0


@pytest.mark.asyncio
async def test_get_notes_analytics_not_found(
        client: AsyncClient,
        db_session: AsyncSession,
        jwt_manager: JWTAuthManager
):
    """
    Test the scenario when no notes are found in the database.
    """
    user = await create_user(db_session)

    token = generate_token(user.id, jwt_manager)

    response = await client.get("/api/v1/analytics/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}
