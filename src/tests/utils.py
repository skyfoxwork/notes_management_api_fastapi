from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.accounts import (
    UserModel,
    UserGroupModel,
    UserGroupEnum
)


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
