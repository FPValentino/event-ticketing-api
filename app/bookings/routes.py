from fastapi import APIRouter, Depends, HTTPException #imports the APIRouter, Depends, and HTTPException classes from the fastapi module, which are used to create a router for event-related routes and to handle dependency injection
from sqlalchemy import func #imports the func class for total booking capacity checking
from sqlalchemy.orm import Session #imports the Session class from the sqlalchemy.orm module, which is used to create a database session for interacting with the database

from app.database import get_db #imports the get_db function from the app.database module, which is used to get a database session
from app.models.booking import Booking #imports the Booking model from the app.models.booking module, which is used to interact with the bookings table in the database
from app.schemas.booking import BookingCreate, BookingResponse #imports the BookingCreate and BookingResponse from the app.schemas.booking module, which are used for Pydantic validation of inputs and database responses
from app.auth.security import get_current_user #imports the get_current_user method which will be used to get the user.id
from app.models.user import User #imports the User model from the app.models.user module, which is used to interact with the users table in the database
from app.models.event import Event #imports the Event model from the app.models.event module


router = APIRouter( #creates an instance of the APIRouter class and assigns it to the variable 'router', which will be used to define routes related to bookings
    prefix="/bookings",
    tags=["Bookings"]
)

@router.post("/", response_model=BookingResponse) #defines a POST endpoint for creating bookings with the path "/bookings" and specifies the response model as BookingResponse
def create_booking(booking: BookingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)): #defines an event handler which takes an BookingCreate object, a database session, and a user account as parameters
    event = db.query(Event).filter(Event.id == booking.event_id).first() #queries the database to retrieve the event with the specified ID from the events table

    if not event: #checks if the event with the specified ID was not found
        raise HTTPException( #raises an HTTPException with a 404 status code and a message indicating that the event was not found
            status_code=404,
            detail="Event not found"
        )

    if booking.quantity <= 0: #checks if the event quantity is greater than 0 (not negative also)
        raise HTTPException( #raises an HTTPException with a 404 status code and a message indicating that the event quantity was less than 1
            status_code=400,
            detail="Quantity must be greater than 0"
        )

    total_booked = db.query(func.sum(Booking.quantity)).filter(Booking.event_id == booking.event_id).scalar() or 0 #gets the sum total of all the booked quantity for a specific booking event ID
    remaining_capacity = event.capacity - total_booked #calculates the remaining available tickets for an event using total_booked and the overall event.capacity

    if booking.quantity > remaining_capacity: #checks if the current quantity being booked by the user is greater than the total remaining available capacity
        raise HTTPException( #raises an HTTPException with a 400 status code stating not enough remaining capacity
            status_code=400,
            detail="Not enough tickets available"
        )

    new_booking = Booking( #creates a new instance of booking with the following data
        user_id = current_user.id, #gets the current user id and sets it as the user_id of the new_booking
        event_id = booking.event_id, #gets the event id and sets it as the event_id of booking
        quantity = booking.quantity, #gets the total number of tickets for the booking
        status = "confirmed" #changes the status to confirmed
    )

    db.add(new_booking) #adds the new instance to the bookings table in the database session
    db.commit() #commits the instance to the database session
    db.refresh(new_booking) #refreshes the database to get the updated data

    return new_booking #returns the current booking details

@router.get("/", response_model=list[BookingResponse]) #defines a GET endpoint for retrieving all bookings with the path "/bookings" and specifies the response model as a list of BookingResponse
def get_bookings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)): #defines an event handler which takes in the current database session and the current user as parameters
    bookings = db.query(Booking).filter(Booking.user_id == current_user.id).all() #gets the Booking records of the current user which matches the Booking.user_id

    return bookings #returns the booking records

@router.get("/{booking_id}", response_model=BookingResponse) #defines a GET endpoint for retrieving specific bookings with the path "/bookings/{booking_id}" and specifies the response model as a the pydantic model BookingResponse
def get_booking(booking_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)): #defines an event handler which takes in the current user booking_id and database session as parameters
    booking = db.query(Booking).filter(Booking.id == booking_id).first() #defines a variable booking that takes in the database record of the user with the matching booking_id

    if not booking: #checks if there are records found with matching booking_id
        raise HTTPException( #raises an HTTPException with a 404 status code and a message indicating that the booking was not found
            status_code=404,
            detail="Booking not found"
        )

    if booking.user_id != current_user.id: #checks if the booking record found matches the recorded user ID in the database
        raise HTTPException( #raises an HTTPException with a 403 status code indicating that the current user and the recorded user in the database do not match
            status_code=403,
            detail="You do not have access to this booking"
        )

    return booking #returns the booking record of the user