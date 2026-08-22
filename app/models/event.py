from datetime import datetime #imports the datetime class from the datetime module, which is used to work with dates and times
from sqlalchemy import DateTime, String, Text #imports the DateTime, String, and Text classes from the sqlalchemy module, which are used to define columns in the database models
from sqlalchemy.orm import Mapped, mapped_column, relationship #imports the Mapped, mapped_column, and relationship classes from the sqlalchemy.orm module, which are used to define mapped attributes and relationships in the database models
from app.database import Base #imports the Base class from the app.database module, which is used as the base class for declarative models in SQLAlchemy    

from typing import TYPE_CHECKING #imports the TYPE_CHECKING constant from the typing module, which is used to indicate that certain imports are only needed for type checking and not at runtime

if TYPE_CHECKING: #checks if the code is being type-checked, and if so, imports the Booking class from the app.models.booking module
    from app.models.booking import Booking #imports the Booking class from the app.models.booking module, which represents a booking in the database

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
    bookings: Mapped[list["Booking"]] = relationship(back_populates="event") #define a bookings relationship that establishes a bidirectional relationship between the Event and Booking models, allowing access to the associated bookings for an event