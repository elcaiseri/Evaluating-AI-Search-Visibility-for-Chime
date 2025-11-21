from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    dataset: str = "sustainability"


class QueryResponse(BaseModel):
    answer: str
    time: float
