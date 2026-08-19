from pydantic import BaseModel, ConfigDict #importing BaseModel and ConfigDict from pydantic library
from datetime import datetime #importing datetime class from datetime module

class EventCreate(BaseModel): #defining a class EventCreate that inherits from BaseModel
    name: str #defining a name attribute of type string
    description: str #defining a description attribute of type string
    location: str #defining a location attribute of type string
    date: datetime #defining a date attribute of type datetime
    capacity: int #defining a capacity attribute of type integer

class EventResponse(BaseModel): #defining a class EventResponse that inherits from BaseModel
    id: int #defining an id attribute of type integer
    name: str #defining a name attribute of type string
    description: str #defining a description attribute of type string
    location: str #defining a location attribute of type string
    date: datetime #defining a date attribute of type datetime
    capacity: int #defining a capacity attribute of type integer
    created_at: datetime #defining a created_at attribute of type datetime

    model_config = ConfigDict(from_attributes=True) #defining a model_config attribute that specifies the configuration for the Pydantic model, in this case, it allows the model to be created from attributes of an object