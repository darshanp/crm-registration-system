import secrets
from datetime import datetime, timedelta, timezone
from app.config import get_settings

settings = get_settings()


def generate_verification_token() -> str:
    """Generate a secure random token for email verification."""
    return secrets.token_urlsafe(32)


def is_token_expired(created_at: datetime) -> bool:
    """Check if a verification token has expired."""
    expiry = created_at + timedelta(hours=settings.verification_token_expire_hours)
    return datetime.now(timezone.utc) > expiry
