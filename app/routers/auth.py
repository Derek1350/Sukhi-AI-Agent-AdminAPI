from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# We need to import models and our dependency
from .. import crud, schemas, security, models
from ..database import get_db
from ..dependencies import get_current_admin

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates a user and returns a JWT access token.
    """
    admin = crud.get_admin_by_username(db, username=form_data.username)
    
    if not admin or not security.verify_password(form_data.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = security.create_access_token(
        data={"sub": admin.username}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.Admin)
def read_users_me(current_admin: models.Admin = Depends(get_current_admin)):
    """
    Get the current logged-in admin's details.
    
    This endpoint is used by the frontend to verify if the JWT is still valid.
    If the token is invalid or expired, it will automatically return a 401 error.
    """
    return current_admin