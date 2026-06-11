from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL format: postgresql://username:password@host:port/database_name
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost:5432/bamburi"

# Create the engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our database models to inherit from
Base = declarative_base()

# Dependency to get a DB session for each API request, and close it when done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
