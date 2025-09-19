from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db
from ..dependencies import get_current_admin

router = APIRouter(
    prefix="/sukhi-profile",
    tags=["Sukhi Profile"],
    dependencies=[Depends(get_current_admin)],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=schemas.SukhiProfile)
def read_sukhi_profile(db: Session = Depends(get_db)):
    """
    Retrieve the global Sukhi profile.
    """
    return crud.get_sukhi_profile(db)

@router.put("/", response_model=schemas.SukhiProfile)
def update_sukhi_profile_details(
    profile_update: schemas.SukhiProfileUpdate, db: Session = Depends(get_db)
):
    """
    Update the global Sukhi profile's details.
    """
    return crud.update_sukhi_profile(db, profile_update=profile_update)
