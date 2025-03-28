from fastapi import FastAPI
from api.routes import router

app = FastAPI()

# Include API routes
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome to the News Sentiment Analyzer API"}
