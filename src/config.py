from pydantic import BaseSettings, PostgresDsn

class Settings(BaseSettings):
    database_uri: str | PostgresDsn = None

    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()
