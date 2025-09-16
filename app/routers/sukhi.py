# Uncomment the following imports when you are ready to enable S3 photo uploads
# from fastapi import File, UploadFile
# import boto3
# from botocore.exceptions import NoCredentialsError
# from ..config import settings

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
#         object_name = file.filename
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
    prefix="/sukhi",
    tags=["Sukhi Profile"],
    dependencies=[Depends(get_current_admin)],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=schemas.Sukhi)
def read_sukhi_profile(db: Session = Depends(get_db)):
    """
    Retrieve Sukhi's full profile, including assigned prompts.
    Requires admin authentication.
    """
    return crud.get_sukhi_profile(db)

@router.put("/", response_model=schemas.Sukhi)
def update_sukhi_details(sukhi_update: schemas.SukhiUpdate, db: Session = Depends(get_db)):
    """
    Update Sukhi's profile details (name, about, photo_url).
    To update the photo, include a "photo_url" key with a dummy URL in the request body.
    Requires admin authentication.
    """
    return crud.update_sukhi_profile(db, sukhi_update=sukhi_update)


# ==============================================================================
# S3 Photo Upload Endpoint (Commented out for future use)
# ==============================================================================
# @router.post("/upload-photo", response_model=schemas.Sukhi)
# def upload_sukhi_photo(db: Session = Depends(get_db), file: UploadFile = File(...)):
#     """Upload a new photo for Sukhi to S3 and update the profile URL."""
#     if not settings.S3_BUCKET_NAME:
#         raise HTTPException(status_code=500, detail="S3 bucket name is not configured on the server.")
#
#     file_url = upload_file_to_s3(file, settings.S3_BUCKET_NAME)
#    
#     if file_url is None:
#         raise HTTPException(status_code=500, detail="Could not upload file to S3. Check server credentials and configuration.")
#    
#     sukhi_update = schemas.SukhiUpdate(photo_url=file_url)
#     return crud.update_sukhi_profile(db, sukhi_update=sukhi_update)
# ==============================================================================


@router.post("/assign-prompt/{prompt_id}", response_model=schemas.Sukhi)
def assign_prompt(prompt_id: int, db: Session = Depends(get_db)):
    """
    Assign an existing prompt to Sukhi.
    Requires admin authentication.
    """
    db_prompt = crud.get_prompt(db, prompt_id=prompt_id)
    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return crud.assign_prompt_to_sukhi(db, prompt_id=prompt_id)

@router.delete("/remove-prompt/{prompt_id}", response_model=schemas.Sukhi)
def remove_prompt(prompt_id: int, db: Session = Depends(get_db)):
    """
    Remove a prompt assignment from Sukhi.
    Requires admin authentication.
    """
    db_prompt = crud.get_prompt(db, prompt_id=prompt_id)
    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found, cannot remove assignment")
    return crud.remove_prompt_from_sukhi(db, prompt_id=prompt_id)