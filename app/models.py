from sqlalchemy import Column, Integer, String, Text, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

# Association Table Updated: prompt_id is now a String
agent_prompt_association = Table(
    'agent_prompt_association',
    Base.metadata,
    Column('agent_id', String, ForeignKey('agents.id'), primary_key=True),
    Column('prompt_id', String, ForeignKey('prompts.id'), primary_key=True)
)

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class SukhiProfile(Base):
    """
    Represents the top-level Sukhi profile. Enforced as a single row.
    """
    __tablename__ = "sukhi_profile"
    id = Column(Integer, primary_key=True, default=1)
    name = Column(String, default="Sukhi", nullable=False)
    about = Column(Text, nullable=True)
    photo_url = Column(String, nullable=True)

class Agent(Base):
    __tablename__ = "agents"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    about = Column(Text, nullable=True)
    photo_url = Column(String, nullable=True)
    prompts = relationship(
        "Prompt",
        secondary=agent_prompt_association,
        back_populates="assigned_to_agents"
    )

class Prompt(Base):
    """
    Represents an AI prompt with a custom, user-provided primary key.
    """
    __tablename__ = "prompts"
    id = Column(String, primary_key=True, index=True) # <-- Changed to String
    title = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    assigned_to_agents = relationship(
        "Agent",
        secondary=agent_prompt_association,
        back_populates="prompts"
    )

