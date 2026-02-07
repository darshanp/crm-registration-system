from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date
from typing import Optional
import re


class UserCreate(BaseModel):
    """Schema for user registration."""

    name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    date_of_birth: date
    country_code: str = Field(..., pattern=r"^\+\d{1,4}$")
    phone_number: str = Field(..., min_length=7, max_length=15)

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v):
        """Validate phone number contains only digits."""
        if not re.match(r"^\d+$", v):
            raise ValueError("Phone number must contain only digits")
        return v

    @field_validator("date_of_birth")
    @classmethod
    def validate_age(cls, v):
        """Validate user is at least 18 years old."""
        from datetime import date
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 18:
            raise ValueError("User must be at least 18 years old")
        return v


class UserResponse(BaseModel):
    """Schema for user response."""

    id: int
    name: str
    email: str
    email_verified: bool
    date_of_birth: date
    country_code: str
    phone_number: str
    phone_verified: bool
    profile_picture_url: Optional[str] = None
    verified: bool
    is_active: bool

    class Config:
        from_attributes = True
