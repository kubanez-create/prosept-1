from pydantic import BaseModel


class StatisticsDTO(BaseModel):
    id: int
    name: str
    matched: int
    unmatched: int
