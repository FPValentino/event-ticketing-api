from pydantic import BaseModel #importing BaseModel from pydantic library
from datetime import datetime #importing datetime class from datetime module

class UserCreate(BaseModel): #defining a class UserCreate that inherits from BaseModel
    name: str #defining a name attribute of type string
    email: str #defining an email attribute of type string
    password: str #defining a password attribute of type string

class UserResponse(BaseModel): #defining a class UserResponse that inherits from BaseModel
    id: int #defining an id attribute of type integer
    name: str #defining a name attribute of type string
    email: str #defining an email attribute of type string
    role: str #defining a role attribute of type string
    created_at: datetime #defining a created_at attribute of type datetime