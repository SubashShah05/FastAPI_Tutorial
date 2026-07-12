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

# Create session (DB operation ke liye) (CRUD)
sessionLocal = sessionmaker(bind=engine)

# Base (model ke liye)
Base = declarative_base()

# Table(Model)
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


#Create API
@app.post("/todos")
def create_todo(title:str,db:Session = Depends(get_db)):
    new_todo = Todo(title=title, description="", completed="False")
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return{
        "message":"Todo created successfully",
        "data":new_todo
    }
