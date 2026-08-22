from datetime import datetime #imports the datetime class from the datetime module, which is used to work with dates and times
from pydantic import BaseModel, ConfigDict #importing BaseModel and ConfigDict from pydantic library

class BookingCreate(BaseModel): #defining a class BookingCreate that inherits from BaseModel
    event_id: int #defining an event_id attribute of type integer
    quantity: int #defining a quantity attribute of type integer

class BookingResponse(BaseModel): #defining a class BookingResponse that inherits from BaseModel
    id: int #defining an id attribute of type integer
    user_id: int #defining a user_id attribute of type integer
    event_id: int #defining an event_id attribute of type integer
    quantity: int #defining a quantity attribute of type integer 
    status: str #defining a status attribute of type string
    created_at: datetime #defining a created_at attribute of type datetime

    model_config = ConfigDict(from_attributes=True) #defining a model_config attribute that specifies the configuration for the Pydantic model, in this case, it allows the model to be created from attributes of an object