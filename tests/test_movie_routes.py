from unittest.mock import patch

from sqlalchemy.exc import OperationalError, ProgrammingError


class TestMovieRoutes:
    def test_get_movies_with_no_movies_in_database(self, client):
        response = client.get("/movies")
        assert response.status_code == 404
        assert response.json() == {"detail": "Not Found: Unable to find movie in Database"}

    def test_get_movies_with_movies_in_database(self, db_session, client, create_single_mock_movie):
        db_session.add(create_single_mock_movie)
        db_session.commit()

        response = client.get("/movies")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json()["message"] == "Movie data retrieved from database"
        assert response.json()["data"][0]["title"] == "Mock Movie Title"

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
