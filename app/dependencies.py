from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from . import crud, schemas, models
from .database import get_db
from .config import settings
from .security import ALGORITHM

# This tells FastAPI that the token should be sent in the header as:
# Authorization: Bearer <your_token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_admin(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> models.Admin:
    """
    Decodes the JWT token to get the current user.
    This function will be used as a dependency in protected endpoints.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    # Get the admin from the database
    admin = crud.get_admin_by_username(db, username=token_data.username)
    if admin is None:
        raise credentials_exception
        
    return admin