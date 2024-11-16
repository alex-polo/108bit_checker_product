import os

from environs import Env

from src.config.classes import AuthConfig


def get_auth_config() -> AuthConfig:
    env = Env()
    env.read_env(os.path.join(os.getcwd(), '.env'))

    return AuthConfig(
        auth_secret_key=env.str('AUTH_SECRET_KEY')
    )