from datetime import datetime #imports the datetime class from the datetime module, which is used to work with dates and times

from sqlalchemy import DateTime, String #imports the DateTime and String classes from the sqlalchemy module, which are used to define columns in the database models
from sqlalchemy.orm import Mapped, mapped_column #imports the Mapped and mapped_column classes from the sqlalchemy.orm module, which are used to define mapped attributes in the database models   

from app.database import Base #imports the Base class from the app.database module, which is used as the base class for declarative models in SQLAlchemy


class User(Base): #define a User class that inherits from the Base class, representing a user in the database
    __tablename__ = "users" #specify the name of the table in the database that this model represents

    id: Mapped[int] = mapped_column(primary_key=True) #define an id column as the primary key for the users table, which is an integer type
    name: Mapped[str] = mapped_column(String(100)) #define a name column as a string type with a maximum length of 100 characters for the users table
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True) #define an email column as a string type with a maximum length of 255 characters for the users table, which must be unique and indexed
    password_hash: Mapped[str] = mapped_column(String(255)) #define a password_hash column as a string type with a maximum length of 255 characters for the users table, which stores the hashed password of the user
    role: Mapped[str] = mapped_column(String(20), default="user") #define a role column as a string type with a maximum length of 20 characters for the users table, which has a default value of "user"
    created_at: Mapped[datetime] = mapped_column( #define a created_at column as a datetime type for the users table, which stores the timestamp of when the user was created
        DateTime,
        default=datetime.utcnow
    )