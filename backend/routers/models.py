from pydantic import BaseModel
from typing import Any, Dict

class QueryRequest(BaseModel):
    query: str
    dataset : str = 'sustainability'

class QueryResponse(BaseModel):
    answer: str
    time : float