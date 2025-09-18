from pydantic import BaseModel, ConfigDict
from typing import List, Optional
import datetime

# ==================================
# Prompt Schemas (No changes needed)
# ==================================

class PromptBase(BaseModel):
    title: str
    content: str

class PromptCreate(PromptBase):
    pass

class PromptUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class Prompt(PromptBase):
    id: int
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# ==================================
# Agent Schemas (Updated for Custom String ID)
# ==================================

class AgentBase(BaseModel):
    name: str
    about: Optional[str] = None
    photo_url: Optional[str] = None

class AgentCreate(AgentBase):
    # The custom string ID is now required during creation.
    id: str

class AgentUpdate(BaseModel):
    # The ID cannot be updated, so it is not included here.
    name: Optional[str] = None
    about: Optional[str] = None
    photo_url: Optional[str] = None

class Agent(AgentBase):
    # The response model reflects the new string ID.
    id: str
    prompts: List[Prompt] = []

    model_config = ConfigDict(from_attributes=True)


# ==================================
# Admin & Token Schemas (No changes needed)
# ==================================

class AdminBase(BaseModel):
    username: str

class AdminCreate(AdminBase):
    password: str

class Admin(AdminBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

