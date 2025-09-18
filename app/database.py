from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# We will add the pool_pre_ping=True argument here.
# This instructs the engine to test connections for liveness before using them.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get a DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

