from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get("/student/{id}")
def get_student(id:int):
    return {"Student ID": id}

