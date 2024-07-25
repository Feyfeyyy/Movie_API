from typing import Any, List, Optional, Type

from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from app.models.movie import Movie
from app.schemas.base import MovieSchema


class Crud:
    def __init__(self, db: Session):
        self.db = db

    def get_movies_info(
        self,
        title: Optional[str] = None,
        genre: Optional[str] = None,
        year: Optional[str] = None,
    ):
        """
        Get movies from the database that match the given filters (if any) and return them

        :param title: title of the movie
        :param genre: genre of the movie
        :param year: year of the movie
        :return: list of movies that match the given filters
        """
        query = self.db.query(Movie)

        if title is not None:
            query = query.filter(func.lower(Movie.title).contains(title.lower()))
        if genre is not None:
            query = query.filter(func.lower(Movie.genre).contains(genre.lower()))
        if year is not None:
            query = query.filter(func.lower(Movie.year).contains(year.lower()))

        movies = query.all()
        return movies

    def get_movie_rating_by_unique_filter(self, movie_id: int, user_id: int) -> Any:
        """
        Get a movie from the database by its user id and return it to the user in JSON format

        :param movie_id: movie id of the movie to retrieve
        :param user_id: user id of the movie to retrieve
        :return: movie with the given movie id or user id.
        """
        return (
            self.db.query(Movie)
            .filter(Movie.id == movie_id, Movie.user_id == user_id)
            .first()
        )

    def get_movie_average_rating(self, movie: Movie) -> Any:
        """
        Retrieve the top five movie average ratings from the database and return them to the
        user in JSON format

        :param movie: object of the movie
        :return: select average rating of the movie
        """
        return (
            self.db.query(func.avg(Movie.rating))
            .filter(func.lower(Movie.title).contains(movie.title.lower()))
            .scalar()
        )

    def update_movie_rating(self, movie_id: int, user_id: int, rating: int) -> Movie:
        """
        Update the rating of a movie for a given user in the database and return it to the
        user in JSON format

        :param movie_id: id of the movie
        :param user_id: id of the user
        :param rating: rating of the movie
        :return: updated movie rating
        """
        db_rating = self.get_movie_rating_by_unique_filter(movie_id, user_id)
        avr_ratings = self.get_movie_average_rating(db_rating)
        if db_rating:
            db_rating.rating = rating
            db_rating.avr_rating = avr_ratings
            self.db.merge(db_rating)
        db_rating = Movie(
            user_id=user_id,
            rating=rating,
            avr_rating=avr_ratings,
            year=db_rating.year,
            runtime=db_rating.runtime,
            genre=db_rating.genre,
            title=db_rating.title,
        )
        self.db.add(db_rating)

        self.db.commit()
        self.db.refresh(db_rating)
        return db_rating

    def get_top_five_movie_ratings(
        self, user_id: Optional[int] = None
    ) -> list[Type[Movie]]:
        """
        Retrieve the top five movie average ratings from the database. If a user_id is provided,
        it filters the movies to only those associated with the user.

        :param user_id: Optional user id to filter movies
        :return: list of top five movie average ratings
        """
        query = self.db.query(Movie)

        if user_id is not None:
            query = query.filter(Movie.user_id == user_id)

        return query.order_by(desc(Movie.avr_rating)).limit(5).all()

    def get_movie_for_one_user(self, movie_id: int, user_id: int) -> Movie:
        """
        Retrieve the ratings for a given movie from the database for one user only and return them to the
        user in JSON format

        :param movie_id: id of the movie to retrieve
        :param user_id: user id of the movie to retrieve
        :return: movie with the given id and user id
        """
        return (
            self.db.query(Movie)
            .filter(Movie.id == movie_id, Movie.user_id == user_id)
            .first()
        )

    @staticmethod
    def create_movie_schema_list(
        movie_data: List[Type[Movie]], in_list: Optional[bool] = False
    ) -> List[MovieSchema | List[Movie]]:
        """
        Update a list movie with the data from the database and return it to the user in MovieSchema format

        :param movie_data: list containing the movie data
        :param in_list: boolean to return the movie data as a list of dictionaries or MovieSchema
        :return: list of movie data in MovieSchema format or list of dictionaries
        """
        all_movie_list = []
        if in_list:
            for movie in movie_data:
                movie_dict = movie.__dict__
                all_movie_list.append(movie_dict)
            return all_movie_list
        for movie in movie_data:
            movie_dict = movie.__dict__
            all_movie_list.append(MovieSchema(**movie_dict))
        return all_movie_list
