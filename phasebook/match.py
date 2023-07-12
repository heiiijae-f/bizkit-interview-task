import time
from flask import Blueprint

from .data.match_data import MATCHES


# Create a Blueprint for the match endpoint.
bp = Blueprint("match", __name__, url_prefix="/match")


# Define the match endpoint.
@bp.route("<int:match_id>")
def match(match_id):

    # Check if the match id is valid.
    if match_id < 0 or match_id >= len(MATCHES):
        return "Invalid match id", 404

    # Get the start time.
    start = time.time()

    # Check if the two sets of favorite numbers are a match.
    msg = "Match found" if is_match(*MATCHES[match_id]) else "No match"

    # Get the end time.
    end = time.time()

    # Return the response.
    return {"message": msg, "elapsedTime": end - start}


# Define the is_match function.
def is_match(fave_numbers_1, fave_numbers_2):

    # Create sets of the two sets of favorite numbers.
    """
    This function takes two lists of favorite numbers and returns True if all numbers in fave_numbers_2 can be found in fave_numbers_1. Otherwise, it returns False.

    Args:
        fave_numbers_1 (list): The first list of favorite numbers.
        fave_numbers_2 (list): The second list of favorite numbers.

    Returns:
        bool: True if there is a match, False otherwise.
    """

    set_1 = set(fave_numbers_1)
    set_2 = set(fave_numbers_2)

    # Check if set_2 is a subset of set_1.
    return set_2.issubset(set_1)

