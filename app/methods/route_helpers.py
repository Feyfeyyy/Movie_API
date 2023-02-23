from typing import Dict, List


def update_movie_dict(movie_data: Dict, all_movie_list: List) -> List[Dict]:
    """
    Update the movie dictionary with the data from the database and return it to the user in JSON format

    :param movie_data: dictionary containing the movie data
    :param all_movie_list: list of dictionaries containing the movie data
    :return: updated movie dictionary
    """
    movie_dict = movie_data.__dict__

    all_movie_list.append(
        dict(
            id=movie_dict["id"],
            user_id=movie_dict["user_id"],
            title=movie_dict["title"],
            genre=movie_dict["genre"],
            rating=movie_dict["rating"],
            year=movie_dict["year"],
            runtime=movie_dict["runtime"],
            avr_rating=round(movie_dict["avr_rating"], 1),
        )
    )
    return all_movie_list
