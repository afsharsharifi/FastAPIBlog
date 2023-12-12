from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database Config
    database_username: str
    database_password: str
    database_hostname: str
    database_port: str
    database_name: str

    # JWT Confug
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
