from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import pendulum

Base = declarative_base()


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    is_deleted = Column(Boolean, default=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.created_at = pendulum.now("Asia/Bangkok")
        self.updated_at = pendulum.now("Asia/Bangkok")

    def save(self, session):
        self.updated_at = pendulum.now("Asia/Bangkok")
        session.add(self)
        session.commit()
        session.refresh(self)
