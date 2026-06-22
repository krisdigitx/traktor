from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Ecommerce Order Alerts"
    environment: str = "local"

    database_url: str = "sqlite:///./orders.db"
    redis_url: str = "redis://redis:6379/0"

    ebay_client_id: str = ""
    ebay_client_secret: str = ""
    ebay_refresh_token: str = ""
    ebay_marketplace_id: str = "EBAY_GB"

    tiktok_app_key: str = ""
    tiktok_app_secret: str = ""
    tiktok_access_token: str = ""
    tiktok_shop_id: str = ""

    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_whatsapp_from: str = ""
    whatsapp_alert_numbers: str = ""

    dashboard_username: str = "admin"
    dashboard_password: str = "change-me"

    poll_interval_seconds: int = 120
    mock_mode: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
