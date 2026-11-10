from typing import Literal, Optional
from pydantic import BaseModel, Field

class Filter(BaseModel): # defines Filter operation parameters*
    column: str
    op: Literal["=", "!=", ">", "<", "<=", ">=", "in", "like"]
    value: str | float | int | list[str | float | int]

class Metric(BaseModel): # defines Metric operation parameters*
    column: str
    agg: Literal["sum", "avg", "count", "min", "max"]
    alias: Optional[str] = None

class QuerySpec(BaseModel): # LLM decides these
    dimensions: list[str] = Field(default_factory=list)
    metrics: list[Metric] = Field(default_factory=list)
    filters: list[Filter] = Field(default_factory=list)
    order_by: Optional[str] = None
    descending: bool = True
    limit: int = Field(default=100, le=1000)

    

