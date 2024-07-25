from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.orm import Session

from app.database import get_db_session
from app.methods.routes_class import Crud
from app.schemas.responses import MovieResponse

router = APIRouter()


@router.get("/movies", response_model=MovieResponse)
async def pull_movie_info(
    title: str = None,
    genre: str = None,
    year: str = None,
    db: Session = Depends(get_db_session),
) -> Union[HTTPException, MovieResponse]:
    """
    Get movie information from the database that matches the given filters (if any) and return it to the
    user in JSON format
    """
    try:
        movie_crud: Crud = Crud(db)
        db_movie = movie_crud.get_movies_info(title, genre, year)
        if (db_movie is None) or (db_movie == []):
            raise HTTPException(
                status_code=404, detail="Not Found: Unable to find movie in Database"
            )
        final_movie_list = movie_crud.create_movie_schema_list(db_movie)
        return MovieResponse(
            message="Movie data retrieved from database", data=final_movie_list
        )
    except OperationalError:
        raise HTTPException(
            status_code=400,
            detail=f"Bad request: Connection to Database could not be established",
        )
    except ProgrammingError:
        raise HTTPException(
            status_code=400,
            detail=f"Bad request: Movies table does not exist in Database",
        )
