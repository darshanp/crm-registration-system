from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App Config
    app_name: str = "CRM Application"
    environment: str = "development"
    secret_key: str
    frontend_url: str = "http://localhost:8000"
    verification_token_expire_hours: int = 24

    # Database
    database_url: str

    # AWS S3
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_s3_bucket: str = ""
    aws_region: str = "us-east-1"

    # Email (SendGrid)
    sendgrid_api_key: str = ""
    from_email: str = "noreply@example.com"

    # SMS (Twilio - Phase 1b)
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_phone_number: str = ""

    # Stripe (Phase 3)
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""

    # didit.me
    didit_api_key: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
