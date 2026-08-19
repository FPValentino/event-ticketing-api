from app.database import Base, engine #imports the Base class and engine object from the app.database module, which are used to define the base class for declarative models and communicate with the database, respectively
from app.models.user import User #imports the User class from the app.models.user module, which represents a user in the database
from app.models.event import Event #imports the Event class from the app.models.event module, which represents an event in the database

Base.metadata.create_all(bind=engine) #create all the tables defined in the models (in this case, the users table) in the database using the engine object
print("Database tables created successfully!") #print a message indicating that the database tables were created successfully