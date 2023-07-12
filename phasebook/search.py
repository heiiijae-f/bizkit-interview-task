from flask import Blueprint, request
from urllib.parse import urlparse, parse_qs
from functools import cmp_to_key
from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    """
    Searches for users that match the given search parameters.

    Args:
        query_string (str): The query string from the request.

    Returns:
        list: The list of matching users.
    """

    query_string = urlparse(request.url).query
    params = parse_qs(query_string)

    # Get the parameters from the query string.
    id_param = params.get("id")
    name_param = params.get("name")
    age_param = params.get("age")
    occupation_param = params.get("occupation")

    # Initialize the list of filtered users.
    filtered_users = USERS

    # Filter the users by id.
    if id_param:
        user_id = id_param[0]
        filtered_users = [user for user in filtered_users if user["id"] == user_id]

    # Filter the users by name.
    if name_param:
        name = name_param[0].lower()
        filtered_users = [user for user in filtered_users if name in user["name"].lower()]

    # Filter the users by age.
    if age_param:
        age = int(age_param[0])
        filtered_users = [user for user in filtered_users if age - 1 <= user["age"] <= age + 1]

    # Filter the users by occupation.
    if occupation_param:
        occupation = occupation_param[0].lower()
        filtered_users = [user for user in filtered_users if occupation in user["occupation"].lower()]

    def compare_users(user1, user2):
        """
        Sorts the users by id, name, age, and occupation.

        Args:
            user1 (dict): The first user.
            user2 (dict): The second user.

        Returns:
            int: The comparison result.
        """

        # Sort the users by id.
        return (
            -1
            if user1["id"] == user2["id"]
            else 1
            if user2["id"] == user1["id"]
            else (
                -1
                if user1["name"] in user2["name"]
                else 1
                if user2["name"] in user1["name"]
                else (
                    -1
                    if abs(user1["age"] - user2["age"]) <= 1
                    else 1
                    if abs(user2["age"] - user1["age"]) <= 1
                    else 0
                )
            )
        )

    return sorted(filtered_users, key=cmp_to_key(compare_users))

