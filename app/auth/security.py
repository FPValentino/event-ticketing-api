import bcrypt #import bcrypt library for password hashing and verification
import os #import os library for interacting with the operating system
import jwt #import jwt library for creating and verifying JSON Web Tokens (JWT)

from dotenv import load_dotenv #import load_dotenv function from dotenv library to load environment variables from a .env file
from datetime import datetime, timedelta, timezone #import datetime, timedelta, and timezone classes from datetime module for working with dates and times
from fastapi import Depends, HTTPException #import Depends and HTTPException classes from FastAPI library for dependency injection and handling HTTP exceptions
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials #import HTTPBearer and HTTPAuthorizationCredentials classes from fastapi.security module for handling HTTP bearer token authentication
from sqlalchemy.orm import Session #import Session class from SQLAlchemy ORM module for interacting with the database
from app.database import get_db #import get_db function from app.database module to get a database session
from app.models.user import User #import User model from app.models.user module to interact with the users table in the database

def hash_password(password: str) -> str: #define a function to hash a password using bcrypt
    password_bytes = password.encode('utf-8') #encode the password string to bytes
    salt = bcrypt.gensalt() #generate a salt for hashing
    hashed_password = bcrypt.hashpw(password_bytes, salt) #hash the password using the generated salt'

    return hashed_password.decode('utf-8') #return the hashed password as a string

def verify_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode('utf-8') #encode the password string to bytes
    hashed_password_bytes = hashed_password.encode('utf-8') #encode the hashed password string to bytes

    return bcrypt.checkpw(password_bytes, hashed_password_bytes) #verify the password against the hashed password and return True if they match, otherwise return False

load_dotenv() #load environment variables from the .env file

SECRET_KEY = os.getenv("SECRET_KEY") #get the secret key from the environment variable (env file) to be used for signing and verifying JWT tokens

if SECRET_KEY is None: #check if the SECRET_KEY environment variable is not set
    raise ValueError("SECRET_KEY environment variable is not set") #raise a ValueError if the SECRET_KEY environment variable is not set

def create_access_token(user_id: int):
    payload = {
        "sub" : str(user_id), #set the subject of the token to the user ID
        "exp" : datetime.now(timezone.utc) + timedelta(minutes=30) #set the expiration time of the token to 30 minutes from now
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256") #encode the payload using the secret key and the HS256 algorithm to create a JWT token
    return token #return the generated JWT token

security = HTTPBearer() #create an instance of the HTTPBearer class to handle HTTP bearer token authentication

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)): #define a function to get the current user based on the provided JWT token and database session
    token = credentials.credentials #get the token from the HTTPAuthorizationCredentials object
    
    try:
        payload = jwt.decode( #decode the JWT token using the secret key and the HS256 algorithm to get the payload
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

    except jwt.InvalidTokenError as exc: #if the token is invalid orhas expired, raise an HTTPException with a 401 status code and a message indicating that the token has expired
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        ) from exc

    user_id = payload.get("sub") #get the user ID from the payload

    if user_id is None: #if the user ID is not found in the payload
        raise HTTPException( #raise an HTTPException with a 401 status code and a message indicating that the token is invalid
            status_code=401,
            detail="Invalid token"
        )

    user = db.query(User).filter(User.id == int(user_id)).first() #query the database to get the user with the given user ID

    if user is None: #if the user is not found in the database
        raise HTTPException( #raise an HTTPException with a 401 status code and a message indicating that the user is not found
            status_code=401,
            detail="User not found"
        )

    return user #return the user object if the token is valid and the user is found in the database