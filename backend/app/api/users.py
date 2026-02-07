from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.email import email_service
from app.services.storage import storage_service
from app.services.didit import didit_service
from app.utils.tokens import generate_verification_token, is_token_expired
from datetime import date
from typing import Optional

router = APIRouter(prefix="/api", tags=["users"])


@router.post("/register", response_model=dict, status_code=201)
async def register_user(
    name: str = Form(...),
    email: str = Form(...),
    date_of_birth: str = Form(...),  # YYYY-MM-DD
    country_code: str = Form(...),
    phone_number: str = Form(...),
    profile_picture: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    """
    Register a new user with profile picture upload.
    """
    # Parse date
    try:
        dob = date.fromisoformat(date_of_birth)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    # Create UserCreate object for validation
    try:
        user_data = UserCreate(
            name=name,
            email=email,
            date_of_birth=dob,
            country_code=country_code,
            phone_number=phone_number,
        )
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Call didit.me stub for identity verification
    verification_result = didit_service.verify_identity({"email": user_data.email, "name": user_data.name})

    # Create user record
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        date_of_birth=user_data.date_of_birth,
        country_code=user_data.country_code,
        phone_number=user_data.phone_number,
        verification_id=verification_result.get("verification_id"),
        verified=verification_result.get("verified", False),
    )

    # Generate email verification token
    verification_token = generate_verification_token()
    new_user.email_verification_token = verification_token

    # Add to database to get user ID
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Handle profile picture upload
    if profile_picture:
        # Validate file type
        allowed_types = ["image/jpeg", "image/png", "image/gif"]
        if profile_picture.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG, PNG, and GIF allowed.")

        # Validate file size (max 5MB)
        file_content = await profile_picture.read()
        if len(file_content) > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large. Maximum size is 5MB.")

        # Upload to S3
        profile_url = storage_service.upload_profile_picture(
            file_content, profile_picture.filename, new_user.id
        )

        if profile_url:
            new_user.profile_picture_url = profile_url
            db.commit()

    # Send verification email
    email_sent = email_service.send_verification_email(
        to_email=new_user.email, token=verification_token, user_name=new_user.name
    )

    return {
        "success": True,
        "user_id": new_user.id,
        "message": "Registration successful! Please check your email to verify your account.",
        "email_sent": email_sent,
    }


@router.get("/verify-email", response_model=dict)
def verify_email(token: str, db: Session = Depends(get_db)):
    """
    Verify user email with token from verification email.
    """
    # Find user with this token
    user = db.query(User).filter(User.email_verification_token == token).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")

    # Check if already verified
    if user.email_verified:
        return {"success": True, "message": "Email already verified"}

    # Check if token expired (based on created_at + 24 hours)
    if is_token_expired(user.created_at):
        raise HTTPException(status_code=400, detail="Verification token has expired")

    # Verify email
    user.email_verified = True
    user.email_verification_token = None  # Clear token after use
    db.commit()

    return {"success": True, "message": "Email verified successfully!"}


@router.get("/country-codes", response_model=dict)
def get_country_codes():
    """
    Get list of country codes for phone number dropdown.
    """
    country_codes = [
        {"code": "+1", "country": "United States/Canada"},
        {"code": "+44", "country": "United Kingdom"},
        {"code": "+91", "country": "India"},
        {"code": "+86", "country": "China"},
        {"code": "+81", "country": "Japan"},
        {"code": "+49", "country": "Germany"},
        {"code": "+33", "country": "France"},
        {"code": "+39", "country": "Italy"},
        {"code": "+34", "country": "Spain"},
        {"code": "+61", "country": "Australia"},
        {"code": "+55", "country": "Brazil"},
        {"code": "+52", "country": "Mexico"},
        {"code": "+7", "country": "Russia"},
        {"code": "+82", "country": "South Korea"},
        {"code": "+27", "country": "South Africa"},
        {"code": "+31", "country": "Netherlands"},
        {"code": "+46", "country": "Sweden"},
        {"code": "+47", "country": "Norway"},
        {"code": "+41", "country": "Switzerland"},
        {"code": "+65", "country": "Singapore"},
    ]

    return {"success": True, "data": country_codes}
