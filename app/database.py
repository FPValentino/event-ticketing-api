import os #imports the os module, which provides a way to interact with the operating system and access environment variables

from dotenv import load_dotenv #imports the load_dotenv function from the dotenv module, which is used to load environment variables from a .env file
from sqlalchemy import create_engine #imports the create_engine function from the sqlalchemy module, which is used to create a connection to the database
from sqlalchemy.orm import sessionmaker #imports the sessionmaker function from the sqlalchemy.orm module, which is used to create a session factory for interacting with the database
from sqlalchemy.orm import DeclarativeBase #imports the DeclarativeBase class from the sqlalchemy.orm module, which is used to define the base class for declarative models in SQLAlchemy

load_dotenv() #load environment variables from the .env file

DATABASE_URL = os.getenv("DATABASE_URL") #get the database URL from the environment variable (env file) to connect to the PostgreSQL database

if DATABASE_URL is None: #check if the DATABASE_URL environment variable is not set
    raise ValueError("DATABASE_URL environment variable is not set") #raise a ValueError if the DATABASE_URL environment variable is not set

engine = create_engine(DATABASE_URL) #communicate with the database PostgreSQL

class Base(DeclarativeBase): #define a base class for declarative models in SQLAlchemy
    pass

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

#with engine.connect() as connection: #establish a connection to the database using the engine object
#    print("Database connection successful!") #print a message indicating that the database connection was successful  