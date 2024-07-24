from typing import List, Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from app.models.movie import Movie


def get_movies_info(
    db: Session,
    title: Optional[str] = None,
    genre: Optional[str] = None,
    year: Optional[str] = None,
) -> List[Movie]:
    """
    Get movies from the database that match the given filters (if any) and return them

    :param db: database session
    :param title: title of the movie
    :param genre: genre of the movie
    :param year: year of the movie
    :return: list of movies that match the given filters
    """
    query = db.query(Movie)

    if title is not None:
        query = query.filter(func.lower(Movie.title).contains(title.lower()))
    if genre is not None:
        query = query.filter(func.lower(Movie.genre).contains(genre.lower()))
    if year is not None:
        query = query.filter(func.lower(Movie.year).contains(year.lower()))

    movies = query.all()
    return movies


def update_movie_rating(db: Session, movie_id: int, user_id: int, rating: int) -> Movie:
    """
    Update the rating of a movie for a given user in the database and return it to the
    user in JSON format

    :param db: database session
    :param movie_id: id of the movie
    :param user_id: id of the user
    :param rating: rating of the movie
    :return: updated movie rating
    """
    db_rating = (
        db.query(Movie).filter(Movie.id == movie_id, Movie.user_id == user_id).first()
    )
    if db_rating.rating:
        avr_ratings = (
            db.query(func.avg(Movie.rating))
            .filter(func.lower(Movie.title).contains(db_rating.title.lower()))
            .scalar()
        )
        db_rating.rating = rating
        db_rating.avr_rating = avr_ratings
        db.merge(db_rating)

    avr_ratings = (
        db.query(func.avg(Movie.rating))
        .filter(func.lower(Movie.title).contains(db_rating.title.lower()))
        .scalar()
    )
    db_rating = Movie(
        user_id=user_id,
        rating=rating,
        avr_rating=avr_ratings,
        year=db_rating.year,
        runtime=db_rating.runtime,
        genre=db_rating.genre,
        title=db_rating.title,
    )
    db.add(db_rating)

    db.commit()
    db.refresh(db_rating)
    return db_rating


def get_top_five_movie_ratings(db: Session) -> List[Movie]:
    """
    Retrieve the top five movie average ratings from the database and return them to the
    user in JSON format

    :param db: database session
    :return: list of top five movie average ratings
    """
    ratings = db.query(Movie).order_by(desc(Movie.avr_rating)).limit(5).all()
    return ratings


def get_top_five_movie_ratings_by_id(db: Session, user_id: int) -> List[Movie]:
    """
    Get a movie from the database by its user id and return it to the user in JSON format

    :param db: database session
    :param user_id: user id of the movie to retrieve
    :return: movie with the given id
    """
    ratings = (
        db.query(Movie)
        .filter(Movie.user_id == user_id)
        .order_by(desc(Movie.avr_rating))
        .limit(5)
        .all()
    )
    return ratings


def get_movie_for_one_user(db: Session, movie_id: int, user_id: int) -> Movie:
    """
    Retrieve the ratings for a given movie from the database for one user only and return them to the
    user in JSON format

    :param db: database session
    :param movie_id: id of the movie to retrieve
    :param user_id: user id of the movie to retrieve
    :return: list of ratings for the given movie
    """
    ratings = (
        db.query(Movie).filter(Movie.id == movie_id, Movie.user_id == user_id).first()
    )
    return ratings
