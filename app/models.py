from sqlalchemy import Column, Integer, String, Text, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

# Association Table Updated: agent_id is now a String to match the new Agent.id
agent_prompt_association = Table(
    'agent_prompt_association',
    Base.metadata,
    Column('agent_id', String, ForeignKey('agents.id'), primary_key=True),
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


class Agent(Base):
    """
    Represents a manageable AI Agent with a custom, user-provided primary key.
    """
    __tablename__ = "agents"

    # The primary key is now a custom string provided by the user during creation.
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    about = Column(Text, nullable=True)
    photo_url = Column(String, nullable=True)

    # Relationship remains the same, but links via the new string-based ID.
    prompts = relationship(
        "Prompt",
        secondary=agent_prompt_association,
        back_populates="assigned_to_agents"
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
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Updated relationship to point to Agent, allowing a prompt to be assigned to many agents
    assigned_to_agents = relationship(
        "Agent",
        secondary=agent_prompt_association,
        back_populates="prompts"
    )

