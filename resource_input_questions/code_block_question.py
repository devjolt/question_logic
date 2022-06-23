from random import choice, randint, shuffle
import re

from question_logic import utility_logic as utl

from . import which_line_in_the_block_causes_an_error
from . import which_line_causes_an_error_because
from . import what_is_the_outcome_from_the_following_code
from . import which_line_best_matches_the_comment
from . import which_random_line_is_valid_or_invalid

def logic(resource):
    code_block_functions = [
        which_line_in_the_block_causes_an_error,
        which_line_causes_an_error_because,
        what_is_the_outcome_from_the_following_code,
        which_line_best_matches_the_comment,
        which_random_line_is_valid_or_invalid,
    ]
    return choice(code_block_functions).logic(resource)