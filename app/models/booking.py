from datetime import datetime #imports the datetime class from the datetime module, which is used to work with dates and times
from sqlalchemy import DateTime, ForeignKey, String #imports the DateTime, ForeignKey, and String classes from the sqlalchemy module, which are used to define columns in the database models
from sqlalchemy.orm import Mapped, mapped_column, relationship #imports the Mapped, mapped_column, and relationship classes from the sqlalchemy.orm module, which are used to define mapped attributes and relationships in the database models
from app.database import Base #imports the Base class from the app.database module, which is used as the base class for declarative models in SQLAlchemy

from typing import TYPE_CHECKING #imports the TYPE_CHECKING constant from the typing module, which is used to indicate that certain imports are only needed for type checking and not at runtime

if TYPE_CHECKING: #checks if the code is being type-checked, and if so, imports the User and Event classes from their respective modules
    from app.models.user import User #imports the User class from the app.models.user module, which represents a user in the database
    from app.models.event import Event #imports the Event class from the app.models.event module, which represents an event in the database

class Booking(Base): #define a Booking class that inherits from the Base class, representing a booking in the database
    __tablename__ = "bookings" #specify the name of the table in the database that this model represents

    id: Mapped[int] = mapped_column(primary_key=True)  #define an id column as the primary key for the bookings table, which is an integer type
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id")) #define a user_id column as a foreign key that references the id column in the users table, which is an integer type
    user: Mapped["User"] = relationship(back_populates="bookings") #define a user relationship that establishes a bidirectional relationship between the Booking and User models, allowing access to the associated user for a booking
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id")) #define an event_id column as a foreign key that references the id column in the events table, which is an integer type
    event: Mapped["Event"] = relationship(back_populates="bookings") #define an event relationship that establishes a bidirectional relationship between the Booking and Event models, allowing access to the associated event for a booking
    quantity: Mapped[int] = mapped_column() #define a quantity column as an integer type for the bookings table, which stores the number of tickets booked
    status: Mapped[str] = mapped_column(String(20), default="confirmed") #define a status column as a string type with a maximum length of 20 characters for the bookings table, which stores the status of the booking and defaults to "confirmed"
    created_at: Mapped[datetime] = mapped_column( #define a created_at column as a datetime type for the bookings table, which stores the timestamp of when the booking was created
        DateTime,
        default=datetime.utcnow
    )