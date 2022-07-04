from random import choice, randint, shuffle
import re

from question_logic import utility_logic as utl

"""requires pairs
"""

def logic(resource):
    raw_question_0 = resource['question_with_0']
    raw_question_1 = resource['question_with_1']
    pairs, fillers = resource['pairs'], resource['fillers']

    used = []
    id = 1
    items = []
    chosen_pair = choice(list(pairs))
    print(chosen_pair)

    item_question_num = (0, 1) if randint(0,1) == 0 else (1, 0)#if 0,1 code goes into question, if 1,0 code is in items
    item_num, question_num = item_question_num[0], item_question_num[1]
    
    if question_num == 0:
        raw_question = raw_question_0
    else:   
        raw_question = raw_question_0 if raw_question_1 == '' else raw_question_1
    #get one correct and incorrect item
    correct_item, question_item = utl.pick_one_many_times(chosen_pair[item_num]), utl.pick_one_many_times(chosen_pair[question_num])
    print('correct item:', correct_item)
    print('question item:', question_item)
    list(pairs).remove(chosen_pair)
    incorrect = [item[item_num] for item in pairs] + [item[item_num] for item in fillers]

    question_template = utl.raw_question_to_template_question(raw_question, question_item)

    comment = False
    if item_num == 0:    
        items, id, used = utl.add_possible_code_item(correct_item, 'correct', items, id, used)
    else:
        id+= 1
        if question_item[0] == '$':
            comment = True
            items.append({'code':'#' + correct_item, 'indicator':'correct', 'id':f'item{id}'})
        else:
            items.append({'item':correct_item, 'indicator':'correct', 'id':f'item{id}'})
        used.append(chosen_pair[item_num])
    
    print('populating')
    items = utl.populate_items(incorrect, items, id, used, comment)
    print('returning')
    return question_template, items