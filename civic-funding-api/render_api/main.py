from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Civic Funding API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Civic Funding API is live!"}

@app.get("/api/funding")
def funding_summary():
    data = {
        "total_funding": 5500000,
        "initiatives": 4,
        "average_impact": 91.2,
        "regions_served": 3
    }
    return data