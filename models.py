from sqlalchemy import *
from sqlalchemy.orm import relationship
from db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255))
    is_active = Column(Boolean, default=False)
    role = Column(Enum('member','admin', name='role_enum'), default='member')
    donation_level = Column(Integer, nullable=True)

    profile = relationship("Profile", back_populates="user", uselist=False)

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    photo_url = Column(String(500))
    full_name = Column(String(200))
    title = Column(String(200))
    phone = Column(String(50))
    linkedin = Column(String(300))
    short_bio = Column(Text)
    location_state = Column(String(2))
    user = relationship("User", back_populates="profile")

class WhitelistEmail(Base):
    __tablename__ = "whitelist_emails"
    id = Column(BigInteger, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    invited_role = Column(Enum('member','admin', name='invited_role_enum'), default='member')
