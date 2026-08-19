from datetime import datetime #imports the datetime class from the datetime module, which is used to work with dates and times

from sqlalchemy import DateTime, String, Text #imports the DateTime, String, and Text classes from the sqlalchemy module, which are used to define columns in the database models
from sqlalchemy.orm import Mapped, mapped_column #imports the Mapped and mapped_column classes from the sqlalchemy.orm module, which are used to define mapped attributes in the database models

from app.database import Base #imports the Base class from the app.database module, which is used as the base class for declarative models in SQLAlchemy    


class Event(Base): #define an Event class that inherits from the Base class, representing an event in the database
    __tablename__ = "events"  #specify the name of the table in the database that this model represents

    id: Mapped[int] = mapped_column(primary_key=True) #define an id column as the primary key for the events table, which is an integer type
    name: Mapped[str] = mapped_column(String(255))  #define a name column as a string type with a maximum length of 255 characters for the events table
    description: Mapped[str] = mapped_column(Text) #define a description column as a text type for the events table, which can store longer text data
    location: Mapped[str] = mapped_column(String(255)) #define a location column as a string type with a maximum length of 255 characters for the events table
    date: Mapped[datetime] = mapped_column(DateTime) #define a date column as a datetime type for the events table, which stores the date and time of the event  
    capacity: Mapped[int] = mapped_column() #define a capacity column as an integer type for the events table, which stores the maximum number of attendees for the event   
    created_at: Mapped[datetime] = mapped_column( #define a created_at column as a datetime type for the events table, which stores the timestamp of when the event was created
        DateTime,
        default=datetime.utcnow
    )