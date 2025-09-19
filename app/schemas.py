from pydantic import BaseModel, ConfigDict
from typing import List, Optional
import datetime

# ==================================
# Sukhi Profile Schemas (New)
# ==================================
class SukhiProfileBase(BaseModel):
    name: str
    about: Optional[str] = None
    photo_url: Optional[str] = None

class SukhiProfileUpdate(BaseModel):
    name: Optional[str] = None
    about: Optional[str] = None
    photo_url: Optional[str] = None

class SukhiProfile(SukhiProfileBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# ==================================
# Prompt Schemas (Updated for Custom String ID)
# ==================================
class PromptBase(BaseModel):
    title: str
    content: str

class PromptCreate(PromptBase):
    id: str # <-- Custom ID required on creation

class PromptUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class Prompt(PromptBase):
    id: str # <-- ID is now a string
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None
    model_config = ConfigDict(from_attributes=True)

# ==================================
# Agent Schemas (No changes needed)
# ==================================
class AgentBase(BaseModel):
    name: str
    about: Optional[str] = None
    photo_url: Optional[str] = None
class AgentCreate(AgentBase):
    id: str
class AgentUpdate(BaseModel):
    name: Optional[str] = None
    about: Optional[str] = None
    photo_url: Optional[str] = None
class Agent(AgentBase):
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

