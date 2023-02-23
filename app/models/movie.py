from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Movie(Base):
    """
    Movie model
    """

    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    title = Column(String, index=True)
    genre = Column(String)
    rating = Column(Integer)
    year = Column(String)
    runtime = Column(String)
    avr_rating = Column(Integer)
