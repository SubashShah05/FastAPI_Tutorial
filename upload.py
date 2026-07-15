from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
import os
import shutil

app = FastAPI()

# -----------------------------
# Step 1: Create uploads folder
# -----------------------------

UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# -----------------------------
# Step 2: Serve Static Files
# URL:
# http://127.0.0.1:8000/files/filename
# -----------------------------

app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")

# -----------------------------
# Step 3: Home API
# -----------------------------

@app.get("/")
def home():
    return {
        "message": "FastAPI File Upload API"
    }

# -----------------------------
# Step 4: Upload File API
# -----------------------------

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected"
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "file_url": f"http://127.0.0.1:8000/files/{file.filename}"
    }

# -----------------------------
# Step 5: Get File URL API
# -----------------------------

@app.get("/file/{filename}")
def get_file(filename: str):

    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    return {
        "filename": filename,
        "file_url": f"http://127.0.0.1:8000/files/{filename}"
    }

# -----------------------------
# Step 6: List Uploaded Files
# -----------------------------

@app.get("/files")
def list_files():

    files = os.listdir(UPLOAD_DIR)

    return {
        "total_files": len(files),
        "files": files
    }

# -----------------------------
# Step 7: Delete File
# -----------------------------

@app.delete("/delete/{filename}")
def delete_file(filename: str):

    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    os.remove(file_path)

    return {
        "message": "File deleted successfully"
    }