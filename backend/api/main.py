from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SentimentRequest(BaseModel):
    company: str

@app.post("/analyze")
def analyze(request: SentimentRequest):
    return {"message": f"Analyzing sentiment for {request.company}"}
