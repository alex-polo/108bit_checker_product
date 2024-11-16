import os

from environs import Env
from .classes import DatabaseConfig, StorageConfig, AdminUserConfig


def get_database_config() -> DatabaseConfig:
    env = Env()
    env.read_env(os.path.join(os.getcwd(), '.env'))

    return DatabaseConfig(
        DB_USER=env.str('DB_USER'),
        DB_PASS=env.str('DB_PASS'),
        DB_HOST=env.str('DB_HOST'),
        DB_PORT=env.str('DB_PORT'),
        DB_NAME=env.str('DB_NAME'),
    )

def get_storage_folder() -> str:
    # return os.path.join(os.getcwd(), 'storage')
    return 'storage'

def get_storage_config() -> StorageConfig:
    env = Env()
    env.read_env(os.path.join(os.getcwd(), '.env'))

    return StorageConfig(
        use_cloud=True if env.str('USE_CLOUD') == 'YES' else False,
        use_local_directory=True if env.str('USE_LOCAL_DIRECTORY') == 'YES' else False,
        url_yandex_disk=env.str('YANDEX_DISK_URL'),
        storage_folder=env.str('LOCAL_DIRECTORY')
    )

def get_admin_user_config() -> AdminUserConfig:
    env = Env()
    env.read_env(os.path.join(os.getcwd(), '.env'))

    return AdminUserConfig(
        ADMIN_USER_LOGIN=env.str('ADMIN_USER_LOGIN'),
        ADMIN_USER_PASSWORD=env.str('ADMIN_USER_PASSWORD')
    )