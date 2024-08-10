import os
from datetime import datetime, timedelta
from uuid import uuid4

import bcrypt
import aiosmtplib
from sqlalchemy.orm import Session
from fastapi import HTTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

from app.models.password_reset import Admin, PasswordReset

load_dotenv()


class PasswordResetService:
    def __init__(self, db: Session):
        self.db = db

    async def request_reset_password(self, admin_email: str) -> None:
        admin = self.db.query(Admin).filter(Admin.email == admin_email).first()
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")

        token = str(uuid4())
        expires_at = datetime.utcnow() + timedelta(hours=1)

        password_reset = PasswordReset(
            admin_id=admin.id, token=token, expires_at=expires_at
        )

        self.db.add(password_reset)
        self.db.commit()

        reset_link = f"{os.getenv('FRONTEND_URL')}/login/reset-password?token={token}"

        # Send email
        await self.send_reset_email(admin_email, reset_link)

    async def send_reset_email(self, admin_email: str, reset_link: str) -> None:
        message = MIMEMultipart("alternative")
        message["Subject"] = "Password Reset Request"
        message["From"] = os.getenv("EMAIL_USER")
        message["To"] = admin_email

        text = f"""
        You requested a password reset. Please use the following link to reset your password:
        {reset_link}
        """
        html = f"""
        <div style="display: none; max-height: 0px; overflow: hidden; mso-hide: all;">
          You requested a password reset. Please use the following link to reset your password.
        </div>
        <div style="font-family: Arial, sans-serif; line-height: 1.6;">
          <h2>Password Reset Request</h2>
          <p>You requested a password reset. Please click the link below to reset your password:</p>
          <a href="{reset_link}" style="display: inline-block; padding: 10px 20px; font-size: 16px; color: #fff; background-color: #007bff; text-decoration: none; border-radius: 5px;">Reset Password</a>
          <p>This link will expire in 1 hour.</p>
          <p>If you did not request a password reset, please ignore this email.</p>
          <p>Thank you,<br>The SWC Team</p>
        </div>
        """

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        await aiosmtplib.send(
            message,
            hostname="smtp.gmail.com",
            port=587,
            start_tls=True,
            username=os.getenv("EMAIL_USER"),
            password=os.getenv("EMAIL_PASS"),
        )

    async def reset_password(self, token: str, newPassword: str) -> None:
        password_reset = (
            self.db.query(PasswordReset).filter(PasswordReset.token == token).first()
        )

        if not password_reset or password_reset.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=400, detail="Token is invalid or has expired"
            )

        admin = self.db.query(Admin).filter(Admin.id == password_reset.admin_id).first()
        hashed_password = bcrypt.hashpw(newPassword.encode("utf-8"), bcrypt.gensalt())
        admin.password = hashed_password.decode("utf-8")

        self.db.commit()
        self.db.delete(password_reset)
        self.db.commit()
