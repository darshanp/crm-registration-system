from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """User model for registration and authentication."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    email_verified = Column(Boolean, default=False)
    email_verification_token = Column(String(255), nullable=True)

    date_of_birth = Column(Date, nullable=False)
    country_code = Column(String(5), nullable=False)
    phone_number = Column(String(20), nullable=False)
    phone_verified = Column(Boolean, default=False)

    profile_picture_url = Column(String(500), nullable=True)

    # Identity verification (didit.me)
    verification_id = Column(String(255), nullable=True)
    verified = Column(Boolean, default=False)

    # Authentication (Phase 2)
    password_hash = Column(String(255), nullable=True)

    # Status
    is_active = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', name='{self.name}')>"
