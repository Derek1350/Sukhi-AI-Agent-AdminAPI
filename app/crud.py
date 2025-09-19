from sqlalchemy.orm import Session
from . import models, schemas, security

# ==================================
# Admin CRUD Functions (No changes)
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
# Sukhi Profile CRUD Functions (New)
# ==================================
def get_sukhi_profile(db: Session):
    profile = db.query(models.SukhiProfile).filter(models.SukhiProfile.id == 1).first()
    if not profile:
        profile = models.SukhiProfile(id=1, name="Sukhi")
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

def update_sukhi_profile(db: Session, profile_update: schemas.SukhiProfileUpdate):
    profile = get_sukhi_profile(db)
    update_data = profile_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile

# ==================================
# Agent CRUD Functions (Replaces Sukhi functions)
# ==================================

def create_agent(db: Session, agent: schemas.AgentCreate):
    """Creates a new AI Agent with a custom string ID."""
    db_agent = models.Agent(**agent.model_dump())
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

def get_agent(db: Session, agent_id: str):
    """Fetches a single agent by its custom string ID."""
    return db.query(models.Agent).filter(models.Agent.id == agent_id).first()

def get_agents(db: Session, skip: int = 0, limit: int = 100):
    """Fetches a list of all agents with pagination."""
    return db.query(models.Agent).offset(skip).limit(limit).all()

def update_agent(db: Session, agent_id: str, agent_update: schemas.AgentUpdate):
    """Updates an existing agent's details."""
    db_agent = get_agent(db, agent_id)
    if db_agent:
        update_data = agent_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_agent, key, value)
        db.commit()
        db.refresh(db_agent)
    return db_agent

def delete_agent(db: Session, agent_id: str):
    """Deletes an agent."""
    db_agent = get_agent(db, agent_id)
    if db_agent:
        db.delete(db_agent)
        db.commit()
    return db_agent

# ==================================
# Prompt CRUD Functions (No changes)
# ==================================

def get_prompt(db: Session, prompt_id: str):
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
# Prompt Assignment Functions (Updated for Agents)
# ==================================

def assign_prompt_to_agent(db: Session, agent_id: str, prompt_id: str):
    """Assigns an existing prompt to a specific agent."""
    agent = get_agent(db, agent_id)
    prompt_to_assign = get_prompt(db, prompt_id)
    
    if agent and prompt_to_assign and prompt_to_assign not in agent.prompts:
        agent.prompts.append(prompt_to_assign)
        db.commit()
        db.refresh(agent)
    return agent

def remove_prompt_from_agent(db: Session, agent_id: str, prompt_id: int):
    """Removes a prompt assignment from a specific agent."""
    agent = get_agent(db, agent_id)
    prompt_to_remove = get_prompt(db, prompt_id)

    if agent and prompt_to_remove and prompt_to_remove in agent.prompts:
        agent.prompts.remove(prompt_to_remove)
        db.commit()
        db.refresh(agent)
    return agent

def get_unassigned_prompts_for_agent(db: Session, agent_id: str):
    """
    Gets all prompts that are not currently assigned to the specified agent.
    """
    agent = get_agent(db, agent_id)
    if not agent:
        return None # Agent not found
    
    all_prompts = get_prompts(db, limit=1000) # Assuming a reasonable limit
    assigned_prompt_ids = {p.id for p in agent.prompts}
    
    unassigned_prompts = [p for p in all_prompts if p.id not in assigned_prompt_ids]
    return unassigned_prompts

