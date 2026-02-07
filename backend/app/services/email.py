from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import get_settings

settings = get_settings()


class EmailService:
    """Service for sending emails via SendGrid."""

    def __init__(self):
        self.client = None
        if settings.sendgrid_api_key:
            self.client = SendGridAPIClient(settings.sendgrid_api_key)

    def send_verification_email(self, to_email: str, token: str, user_name: str) -> bool:
        """
        Send email verification email.

        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.client:
            # SendGrid not configured, print to console for local dev
            verification_url = f"{settings.frontend_url}/verify-email?token={token}"
            print("\n" + "=" * 60)
            print("📧 EMAIL VERIFICATION (SendGrid not configured)")
            print("=" * 60)
            print(f"To: {to_email}")
            print(f"Subject: Verify your email address")
            print(f"\nHi {user_name},")
            print(f"\nPlease verify your email by clicking this link:")
            print(f"{verification_url}")
            print("\nThis link will expire in 24 hours.")
            print("=" * 60 + "\n")
            return True

        try:
            verification_url = f"{settings.frontend_url}/verify-email?token={token}"

            message = Mail(
                from_email=settings.from_email,
                to_emails=to_email,
                subject="Verify your email address",
                html_content=f"""
                <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2>Welcome to {settings.app_name}!</h2>
                    <p>Hi {user_name},</p>
                    <p>Thank you for registering. Please verify your email address by clicking the button below:</p>
                    <p style="margin: 30px 0;">
                        <a href="{verification_url}"
                           style="background-color: #4CAF50; color: white; padding: 12px 24px;
                                  text-decoration: none; border-radius: 4px; display: inline-block;">
                            Verify Email
                        </a>
                    </p>
                    <p>Or copy and paste this link into your browser:</p>
                    <p><a href="{verification_url}">{verification_url}</a></p>
                    <p style="color: #666; font-size: 12px; margin-top: 30px;">
                        This link will expire in 24 hours. If you didn't create an account, please ignore this email.
                    </p>
                </body>
                </html>
                """,
            )

            response = self.client.send(message)
            return response.status_code == 202

        except Exception as e:
            print(f"❌ Email send error: {e}")
            return False


# Singleton instance
email_service = EmailService()
