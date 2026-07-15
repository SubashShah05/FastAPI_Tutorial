from fastapi import FastAPI, Depends, HTTPException, Header
from jose import jwt
from datetime import datetime, timedelta, timezone

app = FastAPI()

SECRET_KEY = "mysecret"
ALGORITHM = "HS256"

#create Token
def create_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({
        "exp": expire
    })

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


#Login API(Token Generate)
@app.post("/login")
def login(username: str, password: str):
    if username != "admin" or password != "1234":
        raise HTTPException(
           status_code=401,
           detail = "Invalid username or password" 
        )
    token = create_token({
        "sub": username
    })
    return{
        "access_token": token
    }

#Token verify
def varify_token(token: str = Header(None)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    

#Protected Route
@app.get("/secure")
def secure_data(user=Depends(varify_token)):
    return {
        "message": "This is a secure Data Accessed",
        "user": user
    }   