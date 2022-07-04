from random import choice, randint, shuffle
import re

from question_logic import utility_logic as utl

"""Takes a correct and an incorrect list, and turns them into a question
Requires at least 4 positive and 4 negative statements
"""

def logic(resource):
    raw_question = resource['question']
    positive, negative = resource['positive'], resource['negative']
    correct, incorrect = resource['correct'], resource['incorrect']
    
    use_in_question = positive if randint(0,1) == 1 else negative
    if use_in_question == positive:
        items = utl.correct_incorrect_helper(correct, incorrect)
        placeholder_str = positive
    else:
        items = utl.correct_incorrect_helper(incorrect, correct)
        placeholder_str = negative
    template_question = utl.raw_question_to_template_question(raw_question, placeholder_str)
    return template_question, items