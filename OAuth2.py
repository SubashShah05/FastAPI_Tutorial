from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

app = FastAPI()

# ---------------- JWT Configuration ----------------

SECRET_KEY = "mysecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# ---------------- Password Hashing ----------------

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------------- OAuth2 ----------------

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ---------------- Dummy Database ----------------

fake_user_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("1234")
    }
}

# ---------------- Password Functions ----------------

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# ---------------- Create JWT Token ----------------

def create_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

# ---------------- Login API ----------------

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = fake_user_db.get(form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password"
        )

    if not verify_password(
        form_data.password,
        user["hashed_password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password"
        )

    access_token = create_token(
        {"sub": form_data.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# ---------------- Verify Token ----------------

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        return username

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired"
        )

# ---------------- Protected Route ----------------

@app.get("/profile")
def profile(current_user: str = Depends(verify_token)):
    return {
        "message": "Welcome",
        "username": current_user
    }

# ---------------- Public Route ----------------

@app.get("/")
def home():
    return {
        "message": "FastAPI JWT Authentication"
    }