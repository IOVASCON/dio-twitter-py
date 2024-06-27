from typing import List
from fastapi import FastAPI
from src.responses import TrendItem
from simulated_data import simulated_trends
import uvicorn

app = FastAPI()

@app.get("/trends", response_model=List[TrendItem])
def get_trends_route():
    return simulated_trends

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
