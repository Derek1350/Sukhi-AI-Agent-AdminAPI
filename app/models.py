import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

# Association Table for the Many-to-Many relationship between Sukhi and Prompt
sukhi_prompt_association = Table(
    'sukhi_prompt_association',
    Base.metadata,
    Column('sukhi_id', Integer, ForeignKey('sukhi.id'), primary_key=True),
    Column('prompt_id', Integer, ForeignKey('prompts.id'), primary_key=True)
)


class Admin(Base):
    """
    Represents an admin user in the database.
    """
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Sukhi(Base):
    """
    Represents Sukhi's profile information.
    Designed to hold a single row for the main AI agent.
    """
    __tablename__ = "sukhi"

    id = Column(Integer, primary_key=True, index=True, default=1)
    name = Column(String, default="Sukhi", nullable=False)
    about = Column(Text, nullable=True)
    photo_url = Column(String, nullable=True) # URL from Amazon S3

    # Many-to-many relationship with Prompt
    prompts = relationship(
        "Prompt",
        secondary=sukhi_prompt_association,
        back_populates="assigned_to_sukhi"
    )


class Prompt(Base):
    """
    Represents an AI prompt in the database.
    """
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_onupdate=func.now())

    # Many-to-many relationship with Sukhi
    assigned_to_sukhi = relationship(
        "Sukhi",
        secondary=sukhi_prompt_association,
        back_populates="prompts"
    )
