from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from passlib.context import CryptContext
import jwt

fake_db = {"users": {}}

app = FastAPI()


class Payload(BaseModel):
    numbers: List[int]


class BinarySearchPayload(BaseModel):
    numbers: List[int]
    target: int


class BubbleSortPayload(BaseModel):
    numbers: List[int]

class FilterEvenPayload(BaseModel):
    numbers: List[int]

class SumElementsPayload(BaseModel):
    numbers: List[int]

@app.post("/bubble-sort")
async def bubble_sort(payload: BubbleSortPayload):
    numbers = payload.numbers
    n = len(numbers)
    for i in range(n):
        for j in range(0, n - i - 1):
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
    return {"numbers": numbers}

@app.post("/filter-even")
async def filter_even(payload: FilterEvenPayload):
    even_numbers = [num for num in payload.numbers if num % 2 == 0]
    return {"even_numbers": even_numbers}

@app.post("/sum-elements")
async def sum_elements(payload: SumElementsPayload):
    total_sum = sum(payload.numbers)
    return {"sum": total_sum}