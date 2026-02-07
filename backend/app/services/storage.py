import boto3
from botocore.exceptions import ClientError
from app.config import get_settings
from typing import Optional
import uuid
from pathlib import Path

settings = get_settings()


class StorageService:
    """Service for handling file uploads to S3."""

    def __init__(self):
        self.s3_client = None
        if settings.aws_access_key_id and settings.aws_secret_access_key:
            self.s3_client = boto3.client(
                "s3",
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
                region_name=settings.aws_region,
            )

    def upload_profile_picture(self, file_content: bytes, filename: str, user_id: int) -> Optional[str]:
        """
        Upload profile picture to S3.

        Returns:
            S3 URL of uploaded file, or None if S3 is not configured
        """
        if not self.s3_client:
            # S3 not configured, return None (for local dev without AWS)
            print("⚠️  S3 not configured. Skipping profile picture upload.")
            return None

        try:
            # Generate unique filename
            extension = Path(filename).suffix
            s3_key = f"profiles/user-{user_id}-{uuid.uuid4()}{extension}"

            # Upload to S3
            self.s3_client.put_object(
                Bucket=settings.aws_s3_bucket,
                Key=s3_key,
                Body=file_content,
                ContentType=self._get_content_type(extension),
            )

            # Return public URL
            url = f"https://{settings.aws_s3_bucket}.s3.{settings.aws_region}.amazonaws.com/{s3_key}"
            return url

        except ClientError as e:
            print(f"❌ S3 upload error: {e}")
            return None

    @staticmethod
    def _get_content_type(extension: str) -> str:
        """Get content type from file extension."""
        content_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
        }
        return content_types.get(extension.lower(), "application/octet-stream")


# Singleton instance
storage_service = StorageService()
