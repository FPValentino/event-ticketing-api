from fastapi import APIRouter, Depends, HTTPException #import the APIRouter, Depends, and HTTPException classes from the FastAPI library
from sqlalchemy.orm import Session #import the Session class from the SQLAlchemy ORM module

from app.database import get_db #import the get_db function from the app.database module, which is used to get a database session
from app.models.user import User #import the User model from the app.models.user module
from app.schemas.user import UserCreate, UserResponse #import the UserCreate and UserResponse schemas from the app.schemas.user module
from app.auth.security import ( #import the hash_password, verify_password, and create_access_token functions from the app.auth.security module
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

router = APIRouter(
    prefix = "/auth",  # Set the prefix for all routes in this router to "/auth"
    tags = ["Authentication"]  # Tag all routes in this router with "authentication" for documentation purposes
)

@router.post("/register", response_model=UserResponse) #define a POST endpoint for user registration with the path "/register" and specify the response model as UserResponse
def register(user: UserCreate, db: Session = Depends(get_db)): #define a function to handle user registration, which takes a UserCreate object and a database session as parameters
    existing_user = db.query(User).filter(User.email == user.email).first() #query the database to check if a user with the same email already exists

    if existing_user: #if a user with the same email already exists
        raise HTTPException( #raise an HTTPException with a 409 status code and a message indicating that the email is already registered
            status_code=409, 
            detail="Email already registered"
            ) 

    hashed_password = hash_password(user.password) #hash the user's password using the hash_password function

    new_user = User(
        name = user.name, #set the name of the new user to the name provided in the UserCreate object
        email = user.email, #set the email of the new user to the email provided in the UserCreate object
        password_hash = hashed_password, #set the password_hash of the new user to the hashed password
        role = "user" #set the role of the new user to "user"
    )

    db.add(new_user) #add the new user to the database session
    db.commit() #commit the changes to the database
    db.refresh(new_user) #refresh the new user object to get the updated data from the database

    return new_user #return the new user object as the response

@router.post("/login") #define a POST endpoint for user login with the path "/login"
def login(user: UserCreate, db: Session = Depends(get_db)): #define a function to handle user login, which takes a UserCreate object and a database session as parameters
    existing_user = db.query(User).filter(User.email == user.email).first() #query the database to find a user with the provided email

    if not existing_user: #if no user with the provided email is found
        raise HTTPException( #raise an HTTPException with a 401 status code and a message indicating that the email or password is invalid
            status_code=401, 
            detail="Invalid email or password"
            )

    if not verify_password(user.password, existing_user.password_hash): #verify the provided password against the stored hashed password using the verify_password function
        raise HTTPException( #if the password is invalid, raise an HTTPException with a 401 status code and a message indicating that the email or password is invalid
            status_code=401, 
            detail="Invalid email or password"
            )

    access_token = create_access_token(existing_user.id) #create an access token for the authenticated user using the create_access_token function

    return {
        "access_token": access_token, #return the access token in the response
        "token_type": "bearer" #specify the token type as "bearer"
    }

@router.get("/me", response_model=UserResponse) #define a GET endpoint for retrieving the current user's information with the path "/me" and specify the response model as UserResponse
def get_me(current_user: User = Depends(get_current_user)): #define a function to get the current user's information, which takes the current user object as a parameter using the get_current_user dependency
    return current_user #return the current user object as the response