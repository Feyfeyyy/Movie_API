from pydantic import BaseModel

EXAMPLE_JSON = {
    "id": 1,
    "user_id": 1,
    "title": "Inception",
    "genre": "Sci-Fi",
    "year": 2010,
    "runtime": "148 min",
    "rating": 5,
    "avr_rating": 5,
}


class MovieSchema(BaseModel):
    id: int
    user_id: int
    title: str
    genre: str
    year: int
    runtime: str
    rating: int
    avr_rating: int

    model_config = {"json_schema_extra": {"example": EXAMPLE_JSON}}
