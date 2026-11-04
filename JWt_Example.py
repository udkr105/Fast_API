from datetime import datetime, timedelta, timezone
import os
from typing import Optional
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from pydantic import BaseModel
import uvicorn

# Load environment variables from a .env file
load_dotenv()

# Fetch SECRET_KEY from environment, with a fallback if .env is missing
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
ALGORITHM = "HS256"

# Initialize FastAPI app
app = FastAPI(
    title="JWT Auth Test Server",
    description="A complete single-file FastAPI server for testing JWT authorization and credentials in Postman.",
    version="1.1.0"
)

# FastAPI's built-in Bearer token security scheme
security = HTTPBearer()

# Pydantic model for login request body (requires username and password)
class LoginRequest(BaseModel):
    username: str
    password: str

# 1. Login endpoint to verify credentials and generate a JWT
@app.post("/login", summary="Log in with credentials to receive a JWT token")
def login(request_data: LoginRequest):
    # Verify mock credentials (for testing purposes)
    if request_data.username != "johndoe" or request_data.password != "secret123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password."
        )

    # Define payload (claims) including an expiration time
    payload = {
        "username": request_data.username,
        "role": "admin",
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),  # Token expires in 1 hour
    }

    # Generate the JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "message": "Login successful! Copy the token below.",
        "token": token
    }

# Dependency to verify JWT from Authorization header
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        # Decode and verify the token signature and expiration
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token has expired. Please log in again."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token."
        )

# 2. Protected endpoint requiring a valid JWT
@app.get("/protected", summary="Access a protected route using Bearer token")
def protected_route(user: dict = Depends(verify_token)):
    return {
        "message": "Success! You have accessed a protected route.",
        "user": user
    }

# Run the server directly using python server.py
if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)