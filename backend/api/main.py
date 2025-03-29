from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

class CompanyRequest(BaseModel):
    company: str

@app.post("/analyze")
async def analyze(request: CompanyRequest):
    company_name = request.company

    # Mock response (Replace with actual analysis logic)
    response_data = {
        "Company": company_name,
        "Articles": [
            {
                "Title": f"{company_name}'s Stock Surges",
                "Summary": f"{company_name} sees a massive increase in stock prices.",
                "Sentiment": "Positive",
                "Topics": ["Stock Market", "Growth"]
            }
        ],
        "Comparative Sentiment Score": {
            "Sentiment Distribution": {"Positive": 1, "Negative": 0, "Neutral": 0},
            "Topic Overlap": {"Common Topics": ["Stock Market"], "Unique Topics": ["Growth"]}
        },
        "Final Sentiment Analysis": f"{company_name} is experiencing positive news sentiment."
    }

    print("Response Sent to Frontend:", json.dumps(response_data, indent=4))  # Debugging
    return response_data
