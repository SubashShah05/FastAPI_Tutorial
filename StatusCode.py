from fastapi import FastAPI,status,HTTPException

app=FastAPI()

@app.post("/create-user",status_code=status.HTTP_201_CREATED)
def create_user():
    return{
        "message": "User created successfully"
    }


@app.get("/user")
def get_users():
    return{
        "status":"Success",
        "message":"User fetched successfully",
        "data":{
            "name":"John Doe",
            "age":30
        }
    }



@app.get("/user/{user_id}")
def get_user(user_id: int):
    if user_id != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "id": 1,
        "name": "John Doe",
        "age": 30
    }