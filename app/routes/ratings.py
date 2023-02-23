from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.orm import Session

from app.database import get_db_session
from app.methods import sql_alchemy_crud as crud
from app.methods.route_helpers import update_movie_dict
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
        movie_list = []
        db_movie = crud.get_top_five_movie_ratings(db)
        if (db_movie is None) or (db_movie == []):
            raise HTTPException(
                status_code=404, detail="Not Found: No movie found in Database"
            )
        for info in db_movie:
            final_movie_list = update_movie_dict(info, movie_list)
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
        movie_list = []
        user = crud.get_top_five_movie_ratings_by_id(db, user_id)
        if (user is None) or (user == []):
            raise HTTPException(status_code=404, detail="No user found in Database")
        for info in user:
            final_movie_list = update_movie_dict(info, movie_list)
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
    "/movies/user_rating/{movie_id}/{user_id}/{rating}",
    response_model=UpdateRatingResponse,
)
async def update_movie_rating(
    user_id: int, movie_id: int, rating: int, db: Session = Depends(get_db_session)
) -> Union[HTTPException, UpdateRatingResponse]:
    """
    Put endpoint for movies to update the rating of a movie for a specific user
    """
    try:
        if rating < 1 or rating > 5:
            raise HTTPException(
                status_code=400, detail="Rating must be between 1 and 5"
            )
        user = crud.get_movie_for_one_user(db, movie_id, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="No user found in Database")
        rating_result = crud.update_movie_rating(db, user.user_id, user.id, rating)
        return UpdateRatingResponse(
            message=f"Rating value has changed for USER-ID: {user_id} and MOVIE-ID: {movie_id}",
            data=dict(
                movie_id=rating_result.id,
                user_id=rating_result.user_id,
                rating=rating_result.rating,
                average_rating=rating_result.avr_rating,
                title=rating_result.title,
            ),
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
