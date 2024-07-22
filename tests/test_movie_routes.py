class TestMovie:
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