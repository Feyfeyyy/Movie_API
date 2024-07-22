from fastapi import FastAPI

from app.routes.movie_info import router as movie_router
from app.routes.ratings import router as rating_router

app = FastAPI()

app.include_router(movie_router, prefix="/api/v1")
app.include_router(rating_router, prefix="/api/v1")
