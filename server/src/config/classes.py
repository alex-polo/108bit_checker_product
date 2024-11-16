from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str


@dataclass
class StorageConfig:
    use_cloud: bool
    use_local_directory: bool
    url_yandex_disk: str
    storage_folder: str


@dataclass
class AuthConfig:
    auth_secret_key: str

@dataclass
class AdminUserConfig:
    ADMIN_USER_LOGIN: str
    ADMIN_USER_PASSWORD: str