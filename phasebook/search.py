from flask import Blueprint, request
from urllib.parse import urlparse, parse_qs
from functools import cmp_to_key
from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200


def search_users():
    query_string = urlparse(request.url).query
    params = parse_qs(query_string)

    id_param = params.get("id")
    name_param = params.get("name")
    age_param = params.get("age")
    occupation_param = params.get("occupation")

    filtered_users = USERS

    if id_param:
        user_id = id_param[0]
        filtered_users = [user for user in filtered_users if user["id"] == user_id]

    if name_param:
        name = name_param[0].lower()
        filtered_users = [user for user in filtered_users if name in user["name"].lower()]

    if age_param:
        age = int(age_param[0])
        filtered_users = [user for user in filtered_users if age - 1 <= user["age"] <= age + 1]

    if occupation_param:
        occupation = occupation_param[0].lower()
        filtered_users = [user for user in filtered_users if occupation in user["occupation"].lower()]

    return filtered_users
    
    def compare_users(user1, user2):
    if user1["id"] in user2["id"]:
        return -1
    if user2["id"] in user1["id"]:
        return 1
    if user1["name"] in user2["name"]:
        return -1
    if user2["name"] in user1["name"]:
        return 1
    if abs(user1["age"] - user2["age"]) <= 1:
        return -1
    if abs(user2["age"] - user1["age"]) <= 1:
        return 1
    if user1["occupation"] in user2["occupation"]:
        return -1
    if user2["occupation"] in user1["occupation"]:
        return 1
    return 0

return sorted(filtered_users, key=cmp_to_key(compare_users))

