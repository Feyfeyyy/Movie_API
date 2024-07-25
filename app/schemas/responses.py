from typing import List, Optional

from pydantic import BaseModel

from app.schemas.base import EXAMPLE_JSON, MovieSchema


class MovieResponse(BaseModel):
    message: str
    data: Optional[List[MovieSchema]] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Movie data retrieved from database",
                "data": [EXAMPLE_JSON],
            }
        }
    }


class RatingResponse(BaseModel):
    message: str
    data: Optional[List[MovieSchema]] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": f"Top five average rated movies for {EXAMPLE_JSON['user_id']} retrieved from database",
                "data": [EXAMPLE_JSON],
            }
        }
    }


class UpdateRatingResponse(BaseModel):
    message: str
    data: MovieSchema

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": f"Rating value has changed for USER-ID: {EXAMPLE_JSON['user_id']} and MOVIE-ID: {EXAMPLE_JSON['id']}",
                "data": [EXAMPLE_JSON],
            }
        }
    }
