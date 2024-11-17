import contextlib
import logging

from fastapi_users.exceptions import UserAlreadyExists

from src.auth.manager import get_user_manager, get_user_db
from src.auth.schemes import UserCreate
from src.config.classes import AdminUserConfig
from src.config.methods import get_admin_user_config
from src.database import get_async_session

logger = logging.getLogger('server')

async def create_user():
    user_config: AdminUserConfig = get_admin_user_config()
    get_async_session_context = contextlib.asynccontextmanager(get_async_session)
    get_user_db_context = contextlib.asynccontextmanager(get_user_db)
    get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)
    
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        UserCreate(
                            email=user_config.ADMIN_USER_LOGIN,
                            password=user_config.ADMIN_USER_PASSWORD,
                            is_superuser=True,
                            is_active=True,
                            is_verified=True
                        )
                    )
                    logger.info(f"User created {user}")
    except UserAlreadyExists:
        logger.info(f"User {user_config.ADMIN_USER_LOGIN} already exists")

async def up_server():
    await create_user()

