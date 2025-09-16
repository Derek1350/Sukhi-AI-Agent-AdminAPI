from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db
from ..dependencies import get_current_admin

router = APIRouter(
    prefix="/prompts",
    tags=["Prompts"],
    # This dependency applies to ALL endpoints in this router
    dependencies=[Depends(get_current_admin)],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Prompt, status_code=status.HTTP_201_CREATED)
def create_new_prompt(prompt: schemas.PromptCreate, db: Session = Depends(get_db)):
    """
    Create a new AI prompt. Requires admin authentication.
    """
    return crud.create_prompt(db=db, prompt=prompt)

@router.get("/", response_model=List[schemas.Prompt])
def read_all_prompts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of all prompts. Requires admin authentication.
    """
    prompts = crud.get_prompts(db, skip=skip, limit=limit)
    return prompts

@router.get("/{prompt_id}", response_model=schemas.Prompt)
def read_single_prompt(prompt_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single prompt by its ID. Requires admin authentication.
    """
    db_prompt = crud.get_prompt(db, prompt_id=prompt_id)
    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return db_prompt

@router.put("/{prompt_id}", response_model=schemas.Prompt)
def update_existing_prompt(
    prompt_id: int, prompt: schemas.PromptUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing prompt's title or content. Requires admin authentication.
    """
    db_prompt = crud.get_prompt(db, prompt_id=prompt_id)
    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return crud.update_prompt(db=db, prompt_id=prompt_id, prompt_update=prompt)

@router.delete("/{prompt_id}", response_model=schemas.Prompt)
def delete_existing_prompt(prompt_id: int, db: Session = Depends(get_db)):
    """
    Delete a prompt from the database. Requires admin authentication.
    """
    db_prompt = crud.get_prompt(db, prompt_id=prompt_id)
    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    crud.delete_prompt(db=db, prompt_id=prompt_id)
    return db_prompt # Return the deleted item as confirmation