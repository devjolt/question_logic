for name in [
    'which_line_best_matches_the_comment',
    'what_is_the_outcome_from_the_following_code',
    'which_line_causes_an_error_because',
    'which_line_in_the_block_causes_an_error',
    'make_error_line_items_code', 
    'make_outcome_items_code',
    'generic_correct_order',
    'order_from_pairs',
    'multi_option_pairs',
    'new_pairs',
    'posneg_pairs',
    'make_items_question_from_pairs',
    'make_items_question_from_correct_incorrect',
    'multi_option_from_correct_incorrect',
            ]:
    with open(f'{name}.py', 'w+') as f:
        f.writelines(
            [
                'from random import choice, randint, shuffle\n',
                'import re\n\n',
                'from . import utility_logic as utl\n\n\n',
                'def logic(resource):'
                '}'
            ]
        )
