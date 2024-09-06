from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Database credentials
    DATABASE_URL: str

    # AWS Credentials
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str

    # Bucket info
    BUCKET_NAME: str
    INBOUND_FOLDER: str
    OUTBOUND_FOLDER: str
