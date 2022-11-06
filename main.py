from fastapi import FastAPI, File, Depends, FastAPI, HTTPException, status
import sympy 
import cv2
import numpy as np 
import base64
from starlette.responses import StreamingResponse
import io 
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import datetime
import os

app = FastAPI()

security = HTTPBasic()

@app.get("/prime/{number}")
async def is_prime_number(number):
    return {"is_prime": sympy.isprime(int(number))}


@app.post("/picture/invert")
async def UploadImage(file: bytes = File(...)):
    print(type(file))
    nparr = np.fromstring(file, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img_not = cv2.bitwise_not(img)
    _, encoded_img = cv2.imencode('.PNG', img_not)
  
    return StreamingResponse(io.BytesIO(encoded_img.tobytes()), media_type="image/png")

@app.get("/date")
def get_date(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = bytes(os.environ.get("USER"), 'utf-8')
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = bytes(os.environ.get("PASSWORD"), 'utf-8')
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return datetime.datetime.now()
