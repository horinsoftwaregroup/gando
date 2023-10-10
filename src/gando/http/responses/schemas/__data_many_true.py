from pydantic import BaseModel


class DataManyTrueSchema(BaseModel):
    count: int
    next: str | None = None
    previous: str | None = None
    results: list
