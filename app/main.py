from fastapi import FastAPI #imports FastAPI class from the fastapi module
from app.auth.routes import router as auth_router #imports the router object from the app.auth.routes module and renames it to auth_router

app = FastAPI() #creates an instance (object) of the FastAPI class and assigns it to the variable 'app'

@app.get("/") #defines a route for the root endpoint ("/") of the API. When a GET request is made to this endpoint, the function 'root' will be executed.
def root():
    return {"message": "Event Ticketing API"}

app.include_router(auth_router) #includes the auth_router in the main FastAPI application, allowing the authentication routes to be accessible under the "/auth" prefix