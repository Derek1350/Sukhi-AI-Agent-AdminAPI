# Uncomment the following imports when you are ready to enable S3 photo uploads
# from fastapi import File, UploadFile
# import boto3
# from botocore.exceptions import NoCredentialsError
# from ..config import settings


from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db
from ..dependencies import get_current_admin


# ==============================================================================
# S3 Photo Upload Helper Function (Commented out for future use)
# ==============================================================================
# def upload_file_to_s3(file: UploadFile, bucket_name: str, object_name: str = None):
#     """Uploads a file-like object to an S3 bucket."""
#     if object_name is None:
#         # Use a unique name for the file in the bucket to avoid overwrites
#         import uuid
#         object_name = f"agent-photos/{uuid.uuid4()}-{file.filename}"
#
#     s3_client = boto3.client(
#         's3',
#         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
#     )
#     try:
#         s3_client.upload_fileobj(file.file, bucket_name, object_name)
#         # Assumes public-read access is enabled on the bucket
#         url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
#         return url
#     except NoCredentialsError:
#         return None # Credentials not available
#     except Exception as e:
#         return None # Other exceptions
# ==============================================================================



router = APIRouter(
    prefix="/agents",
    tags=["Agents"],
    dependencies=[Depends(get_current_admin)],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Agent, status_code=status.HTTP_201_CREATED)
def create_new_agent(agent: schemas.AgentCreate, db: Session = Depends(get_db)):
    """
    Create a new AI Agent with a custom, user-provided string ID.
    """
    db_agent = crud.get_agent(db, agent_id=agent.id)
    if db_agent:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Agent with ID '{agent.id}' already exists.",
        )
    return crud.create_agent(db=db, agent=agent)

@router.get("/", response_model=List[schemas.Agent])
def read_all_agents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of all agents.
    """
    agents = crud.get_agents(db, skip=skip, limit=limit)
    return agents

@router.get("/{agent_id}", response_model=schemas.Agent)
def read_single_agent(agent_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a single agent by its custom ID.
    """
    db_agent = crud.get_agent(db, agent_id=agent_id)
    if db_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return db_agent

@router.put("/{agent_id}", response_model=schemas.Agent)
def update_existing_agent(
    agent_id: str, agent_update: schemas.AgentUpdate, db: Session = Depends(get_db)
):
    """
    Update an agent's details (name, about, photo_url).
    """
    db_agent = crud.get_agent(db, agent_id=agent_id)
    if db_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return crud.update_agent(db=db, agent_id=agent_id, agent_update=agent_update)

@router.delete("/{agent_id}", response_model=schemas.Agent)
def delete_existing_agent(agent_id: str, db: Session = Depends(get_db)):
    """
    Delete an agent from the database.
    """
    db_agent = crud.get_agent(db, agent_id=agent_id)
    if db_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    crud.delete_agent(db=db, agent_id=agent_id)
    return db_agent

@router.post("/{agent_id}/assign-prompt/{prompt_id}", response_model=schemas.Agent)
def assign_prompt_to_agent_endpoint(agent_id: str, prompt_id: str, db: Session = Depends(get_db)):
    """
    Assign an existing prompt to a specific agent.
    """
    db_agent = crud.get_agent(db, agent_id=agent_id)
    if db_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    db_prompt = crud.get_prompt(db, prompt_id=prompt_id)
    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
        
    return crud.assign_prompt_to_agent(db, agent_id=agent_id, prompt_id=prompt_id)

@router.get("/{agent_id}/unassigned-prompts", response_model=List[schemas.Prompt])
def read_unassigned_prompts(agent_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a list of prompts that are not assigned to this agent.
    """
    unassigned = crud.get_unassigned_prompts_for_agent(db, agent_id=agent_id)
    if unassigned is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return unassigned

@router.delete("/{agent_id}/remove-prompt/{prompt_id}", response_model=schemas.Agent)
def remove_prompt_from_agent_endpoint(agent_id: str, prompt_id: int, db: Session = Depends(get_db)):
    """
    Remove a prompt assignment from a specific agent.
    """
    db_agent = crud.get_agent(db, agent_id=agent_id)
    if db_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")

    # We also check if the prompt exists to provide a clear error message.
    db_prompt = crud.get_prompt(db, prompt_id=prompt_id)
    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
        
    return crud.remove_prompt_from_agent(db, agent_id=agent_id, prompt_id=prompt_id)

# ==============================================================================
# S3 Photo Upload Endpoint for a specific Agent (Commented out for future use)
# ==============================================================================
# @router.post("/{agent_id}/upload-photo", response_model=schemas.Agent)
# def upload_agent_photo(agent_id: str, db: Session = Depends(get_db), file: UploadFile = File(...)):
#     """Upload a new photo for a specific agent to S3 and update the profile URL."""
#     db_agent = crud.get_agent(db, agent_id=agent_id)
#     if db_agent is None:
#         raise HTTPException(status_code=404, detail="Agent not found")
#
#     if not settings.S3_BUCKET_NAME:
#         raise HTTPException(status_code=500, detail="S3 bucket name is not configured on the server.")
#
#     file_url = upload_file_to_s3(file, settings.S3_BUCKET_NAME)
#    
#     if file_url is None:
#         raise HTTPException(status_code=500, detail="Could not upload file to S3. Check server credentials and configuration.")
#    
#     agent_update = schemas.AgentUpdate(photo_url=file_url)
#     return crud.update_agent(db=db, agent_id=agent_id, agent_update=agent_update)
# ==============================================================================
