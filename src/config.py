from pathlib import Path
from functools import lru_cache

from pydantic import BaseSettings, Field, EmailStr
from collections import namedtuple

# Paths:
api_dir = Path(__file__).parent
project_dir = api_dir.parent


class Settings(BaseSettings):
    # API
    API_URL: str = '/api/v1'
    API_NAME: str = 'Ore-Concentrate-API'

    # Routers:
    user_router: str = '/users'
    user_auth_router: str = '/users/auth'
    ore_concentrate_router: str = '/ore_concentrates'
    content_router: str = '/ore_concentrates/content'
    report_router: str = '/ore_concentrates/report'

    # Tags:
    user_tag: list[str] = ['users']
    user_auth_tag: list[str] = ["users auth"]
    ore_concentrate_tag: list[str] = ['ore concentrates']
    content_tag: list[str] = ['ore concentrate content']
    report_tag: list[str] = ['ore concentrate report']

    # Database:
    PG_SUPER_DB: str = Field(..., env='PG_SUPER_DB')
    PG_SUPER_USER: str = Field(..., env='PG_SUPER_USER')
    PG_SUPER_PASSWORD: str = Field(..., env='PG_SUPER_PASSWORD')
    PG_HOST: str = Field(..., env='PG_HOST')
    PG_PORT: str = Field(..., env='PG_PORT')
    PG_USER_DB: str = Field(None, env='PG_USER_DB')
    PG_USER: str = Field(None, env='PG_USER')
    PG_USER_PASSWORD: str = Field(None, env='PG_USER_PASSWORD')
    PG_ROLE: str = Field(None, env='PG_ROLE')

    # Database for tests:
    TEST_DATABASE: dict = {
        'role_name': 'ore_concentrate_test_role',
        'username': 'ore_concentrate_test_user',
        'user_password': '1111',
        'db_name': 'ore_concentrate_test_db'
    }

    # Security:
    # To generate a secure random secret key use the command in your terminal:
    # `openssl rand -hex 32`.
    SECRET_KEY: str = Field(..., env='SECRET_KEY')
    ALGORITHM: str = "HS256"
    TIME_ZONE: str = 'Europe/Moscow'
    ACCESS_TOKEN_EXPIRE_MINUTES = 120
    URL_EXPIRE_HOURS = 2

    # Configuration of sending emails:
    FRONT_URL: str = 'http://0.0.0.0:8000'
    CONFIRM_EMAIL_URL: str = f'{FRONT_URL}' + '/confirm-email/{}/'
    RESET_PASSWORD_URL: str = f'{FRONT_URL}' + '/reset-password/{}/'
    MAIL_USERNAME: str = Field(..., env='MAIL_USERNAME')
    MAIL_PASSWORD: str = Field(..., env='MAIL_PASSWORD')
    MAIL_FROM: EmailStr = Field(..., env='MAIL_FROM')
    MAIL_PORT: int = Field(..., env='MAIL_PORT')
    MAIL_SERVER: str = Field(..., env='MAIL_SERVER')
    MAIL_FROM_NAME: str = Field(..., env='MAIL_FROM_NAME')
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    # REDIS related settings
    REDIS_HOST: str = Field(..., env='REDIS_HOST')
    REDIS_PORT: str = Field(..., env='REDIS_PORT')
    REDIS_PASSWORD: str = Field(..., env='REDIS_PASSWORD')
    REDIS_DB_NUMBER: int = 0

    # CELERY related settings
    CELERY_BROKER_TRANSPORT_OPTIONS: dict = {'visibility_timeout': 3600}
    CELERY_ACCEPT_CONTENT: list = ['application/json']
    CELERY_TASK_SERIALIZER: str = 'json'
    CELERY_RESULT_SERIALIZER: str = 'json'

    class Config:
        env_file = project_dir.joinpath(".env")
        env_file_encoding = 'utf-8'

    def get_psql_db_connection_data(self):
        ConnectionData = namedtuple(
            'PsqlConnectionData', [
                'dbname',
                'user',
                'password',
                'host',
                'port']
        )
        return ConnectionData(self.PG_SUPER_DB,
                              self.PG_SUPER_USER,
                              self.PG_SUPER_PASSWORD,
                              self.PG_HOST,
                              self.PG_PORT)

    def get_database_url(self) -> str:
        """
        Gets the full path to the database.
        :return: URL string.
        """
        return (
            f'postgresql+asyncpg://'
            f'{self.PG_USER}:'
            f'{self.PG_USER_PASSWORD}@'
            f'{self.PG_HOST}:'
            f'{self.PG_PORT}/'
            f'{self.PG_USER_DB}'
        )

    def get_test_database_url(self) -> str:
        """
        Gets the full path to the test database.
        :return: URL string.
        """
        return (
            f"postgresql+asyncpg://"
            f"{self.TEST_DATABASE['username']}:"
            f"{self.TEST_DATABASE['user_password']}@"
            f"{self.PG_HOST}:"
            f"{self.PG_PORT}/"
            f"{self.TEST_DATABASE['db_name']}"
        )

    def get_redis_url(self) -> str:
        """
        Gets the full path to the redis database.
        :return: URL string.
        """
        return (
            f"redis://:"
            f"{self.REDIS_PASSWORD}@"
            f"{self.REDIS_HOST}:"
            f"{self.REDIS_PORT}/"
            f"{self.REDIS_DB_NUMBER}"
        )


@lru_cache()
def get_settings() -> Settings:
    """Gets cached settings."""
    return Settings()
