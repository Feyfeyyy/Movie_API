from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.orm import Session

from app.database import get_db_session
from app.methods.routes_class import Crud
from app.schemas.base import MovieSchema
from app.schemas.responses import RatingResponse, UpdateRatingResponse

router = APIRouter()


@router.get("/movies/top_five/total_user", response_model=RatingResponse)
async def get_top_movies_all_users(
    db: Session = Depends(get_db_session),
) -> Union[HTTPException, RatingResponse]:
    """
    Get endpoint for movies to pull movie data from the database for all users and return the top 5 movies
    """
    try:
        movie_crud: Crud = Crud(db)
        db_movie = movie_crud.get_top_five_movie_ratings()
        if (db_movie is None) or (db_movie == []):
            raise HTTPException(
                status_code=404, detail="Not Found: No movie found in Database"
            )
        final_movie_list = movie_crud.create_movie_schema_list(db_movie, in_list=True)
        sort_top_five_movies = sorted(
            final_movie_list, key=lambda m: (m["avr_rating"], m["title"].lower())
        )
        sort_top_five_movies = sort_top_five_movies[::-1]
        return RatingResponse(
            message="Top five average rated movies for all users retrieved from database",
            data=sort_top_five_movies,
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


@router.get("/movies/top_five/{user_id}", response_model=RatingResponse)
async def get_top_movies_one_user(
    user_id: int, db: Session = Depends(get_db_session)
) -> Union[HTTPException, RatingResponse]:
    """
    Get endpoint for movies to get all movies from the database with their average rating for one user
    """
    try:
        movie_crud: Crud = Crud(db)
        db_movie = movie_crud.get_top_five_movie_ratings(user_id=user_id)
        if (db_movie is None) or (db_movie == []):
            raise HTTPException(status_code=404, detail="No user found in Database")
        final_movie_list = movie_crud.create_movie_schema_list(db_movie, in_list=True)
        sort_top_five_movies = sorted(
            final_movie_list, key=lambda m: (m["avr_rating"], m["title"].lower())
        )
        sort_top_five_movies = sort_top_five_movies[::-1]
        return RatingResponse(
            message=f"Top five average rated movies for {user_id} retrieved from database",
            data=sort_top_five_movies,
        )
    except OperationalError:
        raise HTTPException(
            status_code=400,
            detail=f"Internal Server Error: Connection to Database could not be established",
        )
    except ProgrammingError:
        raise HTTPException(
            status_code=400,
            detail=f"Internal Server Error: Movies table does not exist in Database",
        )


@router.put(
    "/movies/user_rating/{user_id}/{movie_id}/{rating}",
    response_model=UpdateRatingResponse,
)
async def update_movie_rating(
    user_id: int, movie_id: int, rating: int, db: Session = Depends(get_db_session)
) -> Union[HTTPException, UpdateRatingResponse]:
    """
    Put endpoint for movies to update the rating of a movie for a specific user
    """
    try:
        movie_crud: Crud = Crud(db)
        if rating < 1 or rating > 5:
            raise HTTPException(
                status_code=400, detail="Rating must be between 1 and 5"
            )
        user = movie_crud.get_movie_for_one_user(movie_id, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="No user found in Database")
        rating_result = movie_crud.update_movie_rating(user.id, user.user_id, rating)
        return UpdateRatingResponse(
            message=f"Rating value has changed for USER-ID: {user_id} and MOVIE-ID: {movie_id}",
            data=MovieSchema(**rating_result.__dict__),
        )
    except OperationalError:
        raise HTTPException(
            status_code=400,
            detail=f"Internal Server Error: Connection to Database could not be established",
        )
    except ProgrammingError:
        raise HTTPException(
            status_code=400,
            detail=f"Internal Server Error: Movies table does not exist in Database",
        )
