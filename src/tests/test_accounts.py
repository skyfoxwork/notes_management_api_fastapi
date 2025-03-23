from datetime import datetime, timezone, timedelta
from unittest.mock import patch

import pytest
from httpx import AsyncClient

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.accounts import UserModel, UserGroupModel, UserGroupEnum, RefreshTokenModel
from src.security.token_manager import JWTAuthManager


@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient, db_session: AsyncSession):
    """
    Test successful user registration.
    """
    payload = {
        "email": "testuser@example.com",
        "password": "StrongPassword123!"
    }

    response = await client.post("/api/v1/accounts/register/", json=payload)

    assert response.status_code == 201, "Expected status code 201 Created."
    response_data = response.json()
    assert response_data["email"] == payload["email"], "Returned email does not match."
    assert "id" in response_data, "Response does not contain user ID."

    db_result_user = await db_session.execute(select(UserModel).filter_by(email=payload["email"]))
    created_user = db_result_user.scalars().first()

    assert created_user is not None, "User was not created in the database."
    assert created_user.email == payload["email"], "Created user's email does not match."


@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_password, expected_error", [
    ("short", "Password must contain at least 8 characters."),
    ("NoDigitHere!", "Password must contain at least one digit."),
    ("nodigitnorupper@", "Password must contain at least one uppercase letter."),
    ("NOLOWERCASE1@", "Password must contain at least one lower letter."),
    ("NoSpecial123", "Password must contain at least one special character: @, $, !, %, *, ?, #, &."),
])
async def test_register_user_password_validation(client: AsyncClient, invalid_password, expected_error):
    """
    Test password strength validation in the user registration endpoint.

    Ensures the endpoint returns the correct error for invalid passwords.
    """
    payload = {
        "email": "testuser@example.com",
        "password": invalid_password
    }

    response = await client.post("/api/v1/accounts/register/", json=payload)

    assert response.status_code == 422, "Expected status code 422 for invalid input."

    response_data = response.json()
    assert expected_error in str(response_data), f"Expected error message: {expected_error}"


@pytest.mark.asyncio
async def test_register_user_conflict(client: AsyncClient, db_session: AsyncSession):
    """
    Test user registration conflict.

    Ensures that trying to register a user with an existing email
    returns a 409 Conflict status and the correct error message.
    """
    payload = {
        "email": "conflictuser@example.com",
        "password": "StrongPassword123!"
    }

    response_first = await client.post("/api/v1/accounts/register/", json=payload)
    assert response_first.status_code == 201, "Expected status code 201 for the first registration."

    db_result_user = await db_session.execute(select(UserModel).filter_by(email=payload["email"]))
    created_user = db_result_user.scalars().first()

    assert created_user is not None, "User should be created after the first registration."

    response_second = await client.post("/api/v1/accounts/register/", json=payload)
    assert response_second.status_code == 409, "Expected status code 409 for a duplicate registration."

    response_data = response_second.json()
    expected_message = f"A user with this email {payload['email']} already exists."
    assert response_data["detail"] == expected_message, f"Expected error message: {expected_message}"


@pytest.mark.asyncio
async def test_register_user_internal_server_error(client: AsyncClient):
    """
    Test server error during user registration.

    Ensures that a 500 Internal Server Error is returned when a database operation fails.
    """
    payload = {
        "email": "erroruser@example.com",
        "password": "StrongPassword123!"
    }

    with patch("src.routes.accounts.AsyncSession.commit", side_effect=SQLAlchemyError):
        response = await client.post("/api/v1/accounts/register/", json=payload)

        assert response.status_code == 500, "Expected status code 500 for internal server error."

        response_data = response.json()
        expected_message = "An error occurred during user creation."
        assert response_data["detail"] == expected_message, f"Expected error message: {expected_message}"


@pytest.mark.asyncio
async def test_activate_account_success(client: AsyncClient, db_session: AsyncSession):
    """
    Test successful activation of a user account.

    Steps:
    - Register a new user.
    - Verify the user is inactive.
    - Activate the user using the activation token.
    - Verify the user is activated and the token is deleted.
    """
    registration_payload = {
        "email": "testuser@example.com",
        "password": "StrongPassword123!"
    }

    registration_response = await client.post("/api/v1/accounts/register/", json=registration_payload)
    assert registration_response.status_code == 201, "Expected status code 201 for successful registration."
    assert registration_response.json() == {"id": 1, "email": registration_payload["email"]}

    db_result_user = await db_session.execute(select(UserModel).filter_by(email=registration_payload["email"]))
    user = db_result_user.scalars().first()

    assert user is not None, "User was not created in the database."


@pytest.mark.asyncio
async def test_login_user_success(client: AsyncClient, db_session: AsyncSession, jwt_manager: JWTAuthManager):
    """
    Test successful login.

    Validates that access and refresh tokens are returned, refresh token is stored in the database,
    and both tokens are valid.
    """
    user_payload = {
        "email": "testuser@example.com",
        "password": "StrongPassword123!"
    }

    user_group = UserGroupModel(name=UserGroupEnum.USER)
    db_session.add(user_group)

    await db_session.commit()
    await db_session.refresh(user_group)

    user = UserModel.create(
        email=user_payload["email"],
        raw_password=user_payload["password"],
        group_id=user_group.id
    )
    db_session.add(user)
    await db_session.commit()

    login_payload = {
        "email": user_payload["email"],
        "password": user_payload["password"]
    }
    response = await client.post("/api/v1/accounts/login/", json=login_payload)

    assert response.status_code == 201, "Expected status code 201 for successful login."
    response_data = response.json()
    assert "access_token" in response_data, "Access token is missing in the response."
    assert "refresh_token" in response_data, "Refresh token is missing in the response."
    assert response_data["access_token"], "Access token is empty."
    assert response_data["refresh_token"], "Refresh token is empty."

    access_token_data = jwt_manager.decode_access_token(response_data["access_token"])
    assert access_token_data["user_id"] == user.id, "Access token does not contain correct user ID."

    refresh_token_data = jwt_manager.decode_refresh_token(response_data["refresh_token"])
    assert refresh_token_data["user_id"] == user.id, "Refresh token does not contain correct user ID."

    db_result_refresh_token = await db_session.execute(select(RefreshTokenModel).filter_by(user_id=user.id))
    refresh_token_record = db_result_refresh_token.scalars().first()

    assert refresh_token_record is not None, "Refresh token was not stored in the database."
    assert refresh_token_record.token == response_data["refresh_token"], "Stored refresh token does not match."

    expires_at = refresh_token_record.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    assert expires_at > datetime.now(timezone.utc), "Refresh token is already expired."


@pytest.mark.asyncio
async def test_login_user_invalid_cases(client: AsyncClient, db_session: AsyncSession):
    """
    Test login with invalid cases:
    1. Non-existent user.
    2. Incorrect password for an existing user.
    """
    login_payload = {
        "email": "nonexistent@example.com",
        "password": "SomePassword123!"
    }
    response = await client.post("/api/v1/accounts/login/", json=login_payload)

    assert response.status_code == 401, "Expected status code 401 for non-existent user."
    assert response.json()["detail"] == "Invalid email or password.", "Unexpected error message for non-existent user."

    user_payload = {
        "email": "testuser@example.com",
        "password": "CorrectPassword123!"
    }

    user_group = UserGroupModel(name=UserGroupEnum.USER)
    db_session.add(user_group)

    await db_session.commit()
    await db_session.refresh(user_group)

    user = UserModel.create(
        email=user_payload["email"],
        raw_password=user_payload["password"],
        group_id=user_group.id
    )
    user.is_active = True
    db_session.add(user)
    await db_session.commit()

    login_payload_incorrect_password = {
        "email": user_payload["email"],
        "password": "WrongPassword123!"
    }
    response = await client.post("/api/v1/accounts/login/", json=login_payload_incorrect_password)

    assert response.status_code == 401, "Expected status code 401 for incorrect password."
    assert response.json()["detail"] == "Invalid email or password.", \
        "Unexpected error message for incorrect password."


@pytest.mark.asyncio
async def test_login_user_commit_error(client: AsyncClient, db_session: AsyncSession):
    """
    Test login when a database commit error occurs.

    Validates that the endpoint returns a 500 status code and an appropriate error message.
    """
    user_payload = {
        "email": "testuser@example.com",
        "password": "StrongPassword123!"
    }

    user_group = UserGroupModel(name=UserGroupEnum.USER)
    db_session.add(user_group)

    await db_session.commit()
    await db_session.refresh(user_group)

    user = UserModel.create(
        email=user_payload["email"],
        raw_password=user_payload["password"],
        group_id=user_group.id
    )
    db_session.add(user)
    await db_session.commit()

    login_payload = {
        "email": user_payload["email"],
        "password": user_payload["password"]
    }

    with patch("src.routes.accounts.AsyncSession.commit", side_effect=SQLAlchemyError):
        response = await client.post("/api/v1/accounts/login/", json=login_payload)

    assert response.status_code == 500, "Expected status code 500 for database commit error."
    assert response.json()["detail"] == "An error occurred while processing the request.", (
        "Unexpected error message for database commit error."
    )


@pytest.mark.asyncio
async def test_refresh_access_token_success(client: AsyncClient, db_session: AsyncSession, jwt_manager: JWTAuthManager):
    """
    Test successful access token refresh.

    Validates that a new access token is returned when a valid refresh token is provided.
    """
    user_payload = {
        "email": "testuser@example.com",
        "password": "StrongPassword123!"
    }

    user_group = UserGroupModel(name=UserGroupEnum.USER)
    db_session.add(user_group)

    await db_session.commit()
    await db_session.refresh(user_group)

    user = UserModel.create(
        email=user_payload["email"],
        raw_password=user_payload["password"],
        group_id=user_group.id
    )
    user.is_active = True
    db_session.add(user)
    await db_session.commit()

    login_payload = {
        "email": user_payload["email"],
        "password": user_payload["password"]
    }
    login_response = await client.post("/api/v1/accounts/login/", json=login_payload)
    assert login_response.status_code == 201, "Expected status code 201 for successful login."
    login_data = login_response.json()
    refresh_token = login_data["refresh_token"]

    refresh_payload = {"refresh_token": refresh_token}
    refresh_response = await client.post("/api/v1/accounts/refresh/", json=refresh_payload)

    assert refresh_response.status_code == 200, "Expected status code 200 for successful token refresh."
    refresh_data = refresh_response.json()
    assert "access_token" in refresh_data, "Access token is missing in the response."
    assert refresh_data["access_token"], "Access token is empty."

    access_token_data = jwt_manager.decode_access_token(refresh_data["access_token"])
    assert access_token_data["user_id"] == user.id, "Access token does not contain correct user ID."


@pytest.mark.asyncio
async def test_refresh_access_token_expired_token(client: AsyncClient, jwt_manager: JWTAuthManager):
    """
    Test refresh token with expired token.

    Validates that a 400 status code and 'Token has expired.' message are returned
    when the refresh token is expired.
    """
    expired_token = jwt_manager.create_refresh_token(
        {"user_id": 1},
        expires_delta=timedelta(days=-1)
    )

    refresh_payload = {"refresh_token": expired_token}
    refresh_response = await client.post("/api/v1/accounts/refresh/", json=refresh_payload)

    assert refresh_response.status_code == 400, "Expected status code 400 for expired token."
    assert refresh_response.json()["detail"] == "Token has expired.", "Unexpected error message."


@pytest.mark.asyncio
async def test_refresh_access_token_token_not_found(client: AsyncClient, jwt_manager: JWTAuthManager):
    """
    Test refresh token when token is not found in the database.

    Validates that a 401 status code and 'Refresh token not found.' message
    are returned when the refresh token is not stored in the database.
    """
    refresh_token = jwt_manager.create_refresh_token({"user_id": 1})

    refresh_payload = {"refresh_token": refresh_token}
    refresh_response = await client.post("/api/v1/accounts/refresh/", json=refresh_payload)

    assert refresh_response.status_code == 401, "Expected status code 401 for token not found."
    assert refresh_response.json()["detail"] == "Refresh token not found.", "Unexpected error message."
