from typing import List, Union

import uvicorn
from calculation import calculate
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class CalculationResult(BaseModel):
    result: Union[List[float], None]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/calculation", response_model=CalculationResult)
async def calculation(illuminance: str, area: float):
    try:
        result = calculate(illuminance, area)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}
