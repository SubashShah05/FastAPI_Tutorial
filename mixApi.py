from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# put /users/101?nitify=true
# {
#     "name": "John Doe"
#      "age": 30
# }

#define a model for the user data
users=[]

class User(BaseModel):
    name:str
    age:int

@app.post("/users")
def create_user(user: User):
    users.append(user)
    return{
"message": "User created successfully",
        "data": user    
    }

@app.put("/users/{user_id}")
def update_user(user_id: int, user: User, notify: bool = False):
    if user_id < len(users):
        users[user_id] = user

        return {
            "message": "User updated successfully and notification sent",
            "notify": notify,
            "data": user
        }

    return {
        "error": "User not found"
    }