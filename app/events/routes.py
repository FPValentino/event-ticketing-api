from fastapi import APIRouter, Depends, HTTPException #imports the APIRouter, Depends, and HTTPException classes from the fastapi module, which are used to create a router for event-related routes and to handle dependency injection
from sqlalchemy.orm import Session #imports the Session class from the sqlalchemy.orm module, which is used to create a database session for interacting with the database

from app.database import get_db #imports the get_db function from the app.database module, which is used to get a database session
from app.models.event import Event #imports the Event model from the app.models.event module, which is used to interact with the events table in the database
from app.schemas.event import EventCreate, EventResponse #imports the EventCreate and EventResponse schemas from the app.schemas.event module, which are used for request and response validation
from app.auth.security import require_admin #imports the require_admin function from the app.auth.security module, which is used to enforce admin privileges for certain routes
from app.models.user import User #imports the User model from the app.models.user module, which is used to interact with the users table in the database

router = APIRouter( #creates an instance of the APIRouter class and assigns it to the variable 'router', which will be used to define routes related to events
    prefix="/events",
    tags=["Events"]
)

@router.post("/", response_model=EventResponse) #defines a POST endpoint for creating events with the path "/events" and specifies the response model as EventResponse
def create_event(event: EventCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)): #defines a function to handle event creation, which takes an EventCreate object, a database session, and the current user as parameters
    new_event = Event( #creates a new instance of the Event model with the provided event data
        name = event.name, #sets the name of the new event to the name provided in the EventCreate object
        description = event.description, #sets the description of the new event to the description provided in the EventCreate object
        location = event.location, #sets the location of the new event to the location provided in the EventCreate object
        date = event.date, #sets the date of the new event to the date provided in the EventCreate object
        capacity = event.capacity #sets the capacity of the new event to the capacity provided in the EventCreate object
        )

    db.add(new_event) #adds the new event to the database session
    db.commit() #commits the changes to the database
    db.refresh(new_event) #refreshes the new event object to get the updated data

    return new_event #returns the new event object as the response

@router.get("/", response_model=list[EventResponse]) #defines a GET endpoint for retrieving all events with the path "/events" and specifies the response model as a list of EventResponse
def get_events(db: Session = Depends(get_db)): #defines a function to handle retrieving all events, which takes a database session as a parameter
    events = db.query(Event).all() #queries the database to retrieve all events from the events table

    return events #returns the list of events as the response  


@router.get("/{event_id}", response_model=EventResponse) #defines a GET endpoint for retrieving a specific event by its ID with the path "/events/{event_id}" and specifies the response model as EventResponse
def get_event(event_id: int, db: Session = Depends(get_db)): #defines a function to handle retrieving a specific event by its ID, which takes the event ID and a database session as parameters
    event = db.query(Event).filter(Event.id == event_id).first() #queries the database to retrieve the event with the specified ID from the events table

    if not event: #checks if the event with the specified ID was not found
        raise HTTPException( #raises an HTTPException with a 404 status code and a message indicating that the event was not found
            status_code=404,
            detail="Event not found"
        )

    return event #returns the event object as the response


@router.put("/{event_id}", response_model=EventResponse) #defines a PUT endpoint for updating a specific event by its ID with the path "/events/{event_id}" and specifies the response model as EventResponse
def update_event(event_id: int, event: EventCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)): #defines a function to handle updating a specific event by its ID, which takes the event ID, an EventCreate object, a database session, and the current user as parameters
    existing_event = db.query(Event).filter(Event.id == event_id).first() #queries the database to retrieve the event with the specified ID from the events table

    if not existing_event: #checks if the event with the specified ID was not found
        raise HTTPException( #raises an HTTPException with a 404 status code and a message indicating that the event was not found
            status_code=404,
            detail="Event not found"
        )

    existing_event.name = event.name #updates the name of the existing event to the name provided in the EventCreate object
    existing_event.description = event.description #updates the description of the existing event to the description provided
    existing_event.location = event.location #updates the location of the existing event to the location provided
    existing_event.date = event.date #updates the date of the existing event to the date provided
    existing_event.capacity = event.capacity #updates the capacity of the existing event to the capacity provided

    db.commit() #commits the changes to the database
    db.refresh(existing_event) #refreshes the existing event object to get the updated data from the database

    return existing_event #returns the updated event object as the response

@router.delete("/{event_id}") #defines a DELETE endpoint for deleting a specific event by its ID with the path "/events/{event_id}"
def delete_event(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)): #defines a function to handle deleting a specific event by its ID, which takes the event ID, a database session, and the current user as parameters
    existing_event = db.query(Event).filter(Event.id == event_id).first() #queries the database to retrieve the event with the specified ID from the events table

    if not existing_event: #checks if the event with the specified ID was not found
        raise HTTPException( #raises an HTTPException with a 404 status code and a message indicating that the event was not found
            status_code=404,
            detail="Event not found"
        )

    db.delete(existing_event) #deletes the existing event from the database session
    db.commit() #commits the changes to the database

    return {"message": "Event deleted successfully"} #returns a success message as the response
    