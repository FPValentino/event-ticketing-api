from fastapi import FastAPI #imports FastAPI class from the fastapi module

app = FastAPI() #creates an instance (object) of the FastAPI class and assigns it to the variable 'app'

@app.get("/") #defines a route for the root endpoint ("/") of the API. When a GET request is made to this endpoint, the function 'root' will be executed.
def root():
    return {"message": "Event Ticketing API"}