from pydantic import BaseModel, ConfigDict
from typing import List, Optional
import datetime

# ==================================
# Prompt Schemas
# ==================================

class PromptBase(BaseModel):
    """Base schema for a prompt, containing common attributes."""
    title: str
    content: str

class PromptCreate(PromptBase):
    """Schema used for creating a new prompt."""
    pass

class PromptUpdate(BaseModel):
    """Schema used for updating an existing prompt. All fields are optional."""
    title: Optional[str] = None
    content: Optional[str] = None

class Prompt(PromptBase):
    """
    Schema for representing a prompt in API responses.
    Includes database-generated fields like id and timestamps.
    """
    id: int
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None
    
    # This configuration allows the Pydantic model to be created from an ORM model instance.
    model_config = ConfigDict(from_attributes=True)


# ==================================
# Sukhi Schemas
# ==================================

class SukhiBase(BaseModel):
    """Base schema for Sukhi's profile."""
    name: str
    about: Optional[str] = None
    photo_url: Optional[str] = None

class SukhiUpdate(BaseModel):
    """Schema for updating Sukhi's profile. All fields are optional."""
    name: Optional[str] = None
    about: Optional[str] = None
    photo_url: Optional[str] = None # Note: Photo upload is handled separately. This is for URL update.

class Sukhi(SukhiBase):
    """
    Schema for representing Sukhi's profile in API responses.
    Includes the list of prompts assigned to Sukhi.
    """
    id: int
    prompts: List[Prompt] = []

    model_config = ConfigDict(from_attributes=True)


# ==================================
# Admin & Token Schemas
# ==================================

class AdminBase(BaseModel):
    """Base schema for an admin user."""
    username: str

class AdminCreate(AdminBase):
    """Schema for creating a new admin user, requires a password."""
    password: str

class Admin(AdminBase):
    """Schema for representing an admin user in API responses (password is excluded)."""
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """Schema for the JWT access token response."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema for the data encoded within the JWT access token."""
    username: Optional[str] = None
