from fastapi import FastAPI,HTTPException,Request
from fastapi.responses import JSONResponse

app=FastAPI()

class UserNotFoundException(Exception):
    def __init__(self, name:str):
        self.name = name


@app.exception_handler(UserNotFoundException)
def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "status": "Error",
            "message": f"User {exc.name} not found"
            }
    )




@app.get("/users/{name}")
def get_user(name: str):
    if name != "John Doe":
        raise UserNotFoundException(name="John Doe")
    return {
        "id": 1,
        "name": "John Doe",
        "age": 30
    }




# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     if user_id != 1:
#         raise HTTPException(
#             status_code=404,
#             detail="User not found"
#         )

#     return {
#         "id": 1,
#         "name": "John Doe",
#         "age": 30
#     }