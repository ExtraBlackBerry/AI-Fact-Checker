from classes.fact_checker_api import FactCheckerAPI
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

class TextRequest(BaseModel):
    text: str
    url: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/fact_check")
def check_facts(request: TextRequest):
    fact_checker = FactCheckerAPI()
    hi = fact_checker._check_facts(request.text, request.url)
    return hi

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)