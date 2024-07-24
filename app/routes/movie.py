from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.orm import Session

from app.database import get_db_session
from app.methods import sql_alchemy_crud as crud
from app.methods.route_helpers import update_movie_dict
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
        movie_list = []
        db_movie = crud.get_movies_info(db, title, genre, year)
        if (db_movie is None) or (db_movie == []):
            raise HTTPException(
                status_code=404, detail="Not Found: Unable to find movie in Database"
            )
        for info in db_movie:
            final_movie_list = update_movie_dict(info, movie_list)
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
