# Movie API

This is a RESTful API for retrieving information on movies from a database. The API is built 
using Python's FastAPI framework and SQLAlchemy for interacting with the database.

## Features
- Retrieve information on movies from a database.
- Query top five movies based on overall average rating.
- Query top five movies for a user based on their overall average ratings.
- Update movie rating for a user.

## Technology Stack
- Python
- FASTAPI
- SQLAlchemy

## Local Deployment
( Recommended Pycharm For Easier Installation )
- Clone the repository
    ```
    git clone https://github.com/Feyfeyyy/movie-api.git
    ```
- install poetry
    ```python
    pip install poetry
    ```
- create a virtual environment
    ```python
    poetry shell
    ```
- Install the requirements
    ```python
    poetry install
    ```
- Run the application
    ```python
    uvicorn main:app --reload.
    ```

## API Documentation
The API will be available at http://localhost:8000/docs.

## Endpoints

Please see commands.http file for sample requests.


## Error Handling

The API returns appropriate HTTP status codes and error messages for invalid requests. The following errors are handled:

- 404: Not Found (Custom)
- 400: Bad Request (Custom)
- 422: Unprocessable Entity (Internal)
- 500: Internal Server Error (Internal)
