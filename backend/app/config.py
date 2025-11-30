from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/pair_programming"
    
    # Application
    debug: bool = False
    app_name: str = "Pair Programming IDE"
    api_prefix: str = "/api"
    
    # WebSocket
    ws_heartbeat_interval: int = 30  # seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
