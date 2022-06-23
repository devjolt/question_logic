from random import choice, randint, shuffle
import re

from question_logic import utility_logic as utl


def logic(resource):
    '''
    requires
    resource = {
        'question_with_0':'Which isPOSNEG an example of PLACEHOLDER?',
        'question_with_1':'What best describes the following: PLACEHOLDER?',
        'type':['new_pairs'],
        'course_code':'',
        'pairs':[
            ('correct',['A','B','C','D']),
            ('incorrect',['1', '2', '3','4']),
            ('ambiguous',['0', '9', '8','7']),
            ('backwards',['z', 'y', 'x','w']),
        ],
        'fillers': (
            ()
        )
    }
    '''
    pairs=resource['pairs']
    fillers=resource['fillers']
    used = []
    id = 1
    items = []
    chosen_pair = choice(pairs)

    item_question_num = (0, 1) if randint(0,1) == 0 else (1, 0)#if 0,1 code goes into question, if 1,0 code is in items
    item_num, question_num = item_question_num[0], item_question_num[1]
    
    if question_num == 0:
        raw_question = resource['question_with_0']
    else:   
        raw_question = resource['question_with_0'] if resource['question_with_1'] == '' else resource['question_with_1']
    #get one correct and incorrect item
    raw_question=re.sub('POSNEG', '', raw_question)

    correct_item=choice(chosen_pair[item_num]) if type(chosen_pair[item_num])in(list, tuple) else chosen_pair[item_num] 
    question_item=choice(chosen_pair[question_num]) if type(chosen_pair[question_num])in(list, tuple) else chosen_pair[question_num]
            
    list(pairs).remove(chosen_pair)
    incorrect = []
    for pair in pairs:
        if pair[0]!=chosen_pair[0]:
            if type(pair[item_num])in(tuple, list):
                incorrect+=list(pair[item_num])
            else:
                incorrect.append(pair[item_num])
    for pair in fillers:
        if pair[0]!=chosen_pair[0]:
            #print('pair:', pair, 'item_num', item_num)
            if type(pair[item_num]) in (tuple, list):
                incorrect+=list(pair[item_num])
            else:
                incorrect.append(pair)
    
    question_template = utl.raw_question_to_template_question(raw_question, question_item)

    comment = False
    if item_num == 0:    
        items, id, used = utl.add_possible_code_item(correct_item, 'correct', items, id, used)
    else:
        if question_item[0] == '$':
            comment = True
            items.append({'code':'#' + correct_item, 'indicator':'correct', 'id':f'item{id}'})
        else:
            items.append({'item':correct_item, 'indicator':'correct', 'id':f'item{id}'})
        used.append(chosen_pair[item_num])
        id+= 1
   
    items = utl.populate_items(incorrect, items, id, used, comment)
    shuffle(items)
    shuffle(items)
    return question_template, items