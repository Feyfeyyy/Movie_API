from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class MovieResponse(BaseModel):
    message: str
    data: Optional[List[Dict]] = None


class RatingResponse(BaseModel):
    message: str
    data: Optional[List[Dict]] = None


class UpdateRatingResponse(BaseModel):
    message: str
    data: Dict[str, Any]
