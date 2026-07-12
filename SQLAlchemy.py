# Import required libraries
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi import FastAPI, Depends

# Create FastAPI application
app = FastAPI()

# Database URL (SQLite database)
DATABASE_URL = "sqlite:///test.db"

# Create database engine (connection)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create session for database operations (CRUD)
sessionLocal = sessionmaker(bind=engine)

# Base class for all database tables
Base = declarative_base()

# Create Todo table
class Todo(Base):
    __tablename__ = "todos"  # Table name

    id = Column(Integer, primary_key=True, index=True)  # Primary Key
    title = Column(String)          # Todo title
    description = Column(String)    # Todo description
    completed = Column(String)      # Completion status

# Create the table in the database
Base.metadata.create_all(bind=engine)

# Dependency: Open and close database session
def get_db():
    db = sessionLocal()
    try:
        yield db  # Give database session
    finally:
        db.close()  # Close session

# Home API
@app.get("/")
def home(db: Session = Depends(get_db)):
    # Depends(get_db) automatically provides a database session
    return {
        "message": "DB connected fine"
    }