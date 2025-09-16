from sqlalchemy.orm import Session
from . import models, schemas, security

# ==================================
# Admin CRUD Functions
# ==================================

def get_admin_by_username(db: Session, username: str):
    """Fetches an admin user by their username."""
    return db.query(models.Admin).filter(models.Admin.username == username).first()

def create_admin(db: Session, admin: schemas.AdminCreate):
    """Creates a new admin user with a hashed password."""
    hashed_password = security.get_password_hash(admin.password)
    db_admin = models.Admin(username=admin.username, hashed_password=hashed_password)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

# ==================================
# Sukhi CRUD Functions
# ==================================

def get_sukhi_profile(db: Session):
    """
    Fetches Sukhi's profile. If it doesn't exist, it creates a default one.
    """
    sukhi_profile = db.query(models.Sukhi).filter(models.Sukhi.id == 1).first()
    if not sukhi_profile:
        sukhi_profile = models.Sukhi(id=1, name="Sukhi", about="")
        db.add(sukhi_profile)
        db.commit()
        db.refresh(sukhi_profile)
    return sukhi_profile

def update_sukhi_profile(db: Session, sukhi_update: schemas.SukhiUpdate):
    """Updates Sukhi's profile with new data."""
    sukhi_profile = get_sukhi_profile(db)
    update_data = sukhi_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(sukhi_profile, key, value)
    db.commit()
    db.refresh(sukhi_profile)
    return sukhi_profile

# ==================================
# Prompt CRUD Functions
# ==================================

def get_prompt(db: Session, prompt_id: int):
    """Fetches a single prompt by its ID."""
    return db.query(models.Prompt).filter(models.Prompt.id == prompt_id).first()

def get_prompts(db: Session, skip: int = 0, limit: int = 100):
    """Fetches a list of all prompts with pagination."""
    return db.query(models.Prompt).offset(skip).limit(limit).all()

def create_prompt(db: Session, prompt: schemas.PromptCreate):
    """Creates a new prompt."""
    db_prompt = models.Prompt(**prompt.model_dump())
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

def update_prompt(db: Session, prompt_id: int, prompt_update: schemas.PromptUpdate):
    """Updates an existing prompt."""
    db_prompt = get_prompt(db, prompt_id)
    if db_prompt:
        update_data = prompt_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_prompt, key, value)
        db.commit()
        db.refresh(db_prompt)
    return db_prompt

def delete_prompt(db: Session, prompt_id: int):
    """Deletes a prompt."""
    db_prompt = get_prompt(db, prompt_id)
    if db_prompt:
        db.delete(db_prompt)
        db.commit()
    return db_prompt

# ==================================
# Prompt Assignment Functions
# ==================================

def assign_prompt_to_sukhi(db: Session, prompt_id: int):
    """Assigns an existing prompt to Sukhi's profile."""
    sukhi_profile = get_sukhi_profile(db)
    prompt_to_assign = get_prompt(db, prompt_id)
    
    if prompt_to_assign and prompt_to_assign not in sukhi_profile.prompts:
        sukhi_profile.prompts.append(prompt_to_assign)
        db.commit()
        db.refresh(sukhi_profile)
    return sukhi_profile

def remove_prompt_from_sukhi(db: Session, prompt_id: int):
    """Removes a prompt assignment from Sukhi's profile."""
    sukhi_profile = get_sukhi_profile(db)
    prompt_to_remove = get_prompt(db, prompt_id)

    if prompt_to_remove and prompt_to_remove in sukhi_profile.prompts:
        sukhi_profile.prompts.remove(prompt_to_remove)
        db.commit()
        db.refresh(sukhi_profile)
    return sukhi_profile