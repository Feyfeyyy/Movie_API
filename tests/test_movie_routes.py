from unittest.mock import patch

from sqlalchemy.exc import OperationalError, ProgrammingError


class TestMovieRoutes:
    def test_get_movies_with_no_movies_in_database(self, client):
        response = client.get("/movies")
        assert response.status_code == 404
        assert response.json() == {"detail": "Not Found: Unable to find movie in Database"}

    def test_get_movies_with_movies_in_database(self, db_session, client, create_mock_movie):
        db_session.add(create_mock_movie)
        db_session.commit()

        response = client.get("/movies")
        assert response.status_code == 200
        assert response.json() == {
            "message": "Movie data retrieved from database",
            "data": [
                {
                    "id": 1,
                    "user_id": 1,
                    "title": "Test Movie",
                    "genre": "Test Genre",
                    "year": "2021",
                    "runtime": "120 min",
                    "rating": 5,
                    "avr_rating": 5,
                }
            ],
        }

    @patch("app.methods.sql_alchemy_crud.get_movies_info")
    def test_get_movies_with_bad_request(self, mock_get_movies_info, client):
        mock_get_movies_info.side_effect = OperationalError("Mock Operational Error", "", "")
        response = client.get("/movies")
        assert response.status_code == 400
        assert response.json() == {
            "detail": "Bad request: Connection to Database could not be established"
        }

    @patch("app.methods.sql_alchemy_crud.get_movies_info")
    def test_get_movies_with_no_movies_table_found(self, mock_get_movies_info, client):
        mock_get_movies_info.side_effect = ProgrammingError("Mock Programming Error", "", "")
        response = client.get("/movies")
        assert response.status_code == 400
        assert response.json() == {"detail": "Bad request: Movies table does not exist in Database"}
