from fastapi import FastAPI
from pydantic import BaseModel

from postApi import User

app = FastAPI()


#schema for user model
# class User(BaseModel):
#     name: str
#     age: int
#     email: str

#     @app.post("/create-user")
#     def create_user(user: User):
#         return {
#             "message": "User created successfully",
#             "data": user
#         }



#new code with nested model
class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
class User(BaseModel):
    name: str
    age: int
    email: str
    address: Address   

@app.post("/create-user")
def create_user(user:User):
    return {
        "message": "User created successfully",
        "data": user
    }    