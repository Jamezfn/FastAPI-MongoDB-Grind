from pydantic import BaseModel
from typing import Generic, TypeVar, List, Optional
from datetime import datetime

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Wrap any paginated list response."""
    items: List[T]
    next_cursor: Optional[datetime] = None
    limit: int