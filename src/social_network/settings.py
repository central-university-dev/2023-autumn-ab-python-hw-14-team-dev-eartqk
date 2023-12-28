from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, env_file_encoding="utf-8")

    # JWT Auth
    jwt_secret: str = "dont_use_this_key"
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 3600

    # Database
    database_url: str = "postgresql://postgres:postgres@127.0.0.1:5432/homework_db"

    # MinIO
    minio_user: str = "minio_user"
    minio_password: str = "minio_password"
    minio_host: str = "127.0.0.1:9000"


settings = Settings()
