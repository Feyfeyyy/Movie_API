from unittest.mock import patch

from sqlalchemy.exc import OperationalError, ProgrammingError


class TestRatingRoutes:
    def test_get_top_movies_all_users(self, db_session, client, create_mock_movie_list):
        db_session.add_all(create_mock_movie_list)
        db_session.commit()

        response = client.get("/movies/top_five/total_user")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json()["message"] == "Top five average rated movies for all users retrieved from database"
        assert len(response.json()["data"]) == 5

    def test_get_top_movies_one_user(self, db_session, client, create_mock_movie_list):
        db_session.add_all(create_mock_movie_list)
        db_session.commit()
        user_id = create_mock_movie_list[0].user_id
        length = len([movie for movie in create_mock_movie_list if movie.user_id == user_id])

        response = client.get(f"/movies/top_five/{user_id}")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json()["message"] == f"Top five average rated movies for {user_id} retrieved from database"
        assert len(response.json()["data"]) == length

    @patch("app.methods.sql_alchemy_crud.get_top_five_movie_ratings")
    def test_get_top_movies_all_users_with_bad_request(self, mock_get_top_five_movie_ratings, client):
        mock_get_top_five_movie_ratings.side_effect = OperationalError("Mock Operational Error", "", "")
        response = client.get("/movies/top_five/total_user")
        assert response.status_code == 400
        assert response.json() == {
            "detail": "Bad request: Connection to Database could not be established"
        }

    @patch("app.methods.sql_alchemy_crud.get_top_five_movie_ratings")
    def test_get_top_movies_all_users_with_no_movies_table_found(self, mock_get_top_five_movie_ratings, client):
        mock_get_top_five_movie_ratings.side_effect = ProgrammingError("Mock Programming Error", "", "")
        response = client.get("/movies/top_five/total_user")
        assert response.status_code == 400
        assert response.json() == {"detail": "Bad request: Movies table does not exist in Database"}

    @patch("app.methods.sql_alchemy_crud.get_top_five_movie_ratings_by_id")
    def test_get_top_movies_one_user_with_bad_request(self, mock_get_top_five_movie_ratings_by_id, client):
        mock_get_top_five_movie_ratings_by_id.side_effect = OperationalError("Mock Operational Error", "", "")
        response = client.get("/movies/top_five/1")
        assert response.status_code == 400
        assert response.json() == {
            "detail": "Internal Server Error: Connection to Database could not be established"
        }

    @patch("app.methods.sql_alchemy_crud.get_top_five_movie_ratings_by_id")
    def test_get_top_movies_one_user_with_no_movies_table_found(self, mock_get_top_five_movie_ratings_by_id, client):
        mock_get_top_five_movie_ratings_by_id.side_effect = ProgrammingError("Mock Programming Error", "", "")
        response = client.get("/movies/top_five/1")
        assert response.status_code == 400
        assert response.json() == {"detail": "Internal Server Error: Movies table does not exist in Database"}
