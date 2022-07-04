from random import choice, randint, shuffle
import re

from question_logic import utility_logic as utl

def logic(resource):
    '''
    requires:
    resource = {
        'question_with_0':'Which isPOSNEG an example of PLACEHOLDER?',
        'positive_negative':('',' not'),
        'type':['posneg_pairs'],
        'course_code':'',
        'pairs':[
            ('correct',['A','B','C']),
            ('incorrect',['1', '2','3']),#minimum!
        ],
        'fillers': (
        )
    }
    '''
    
    focus_pair = choice(resource['pairs'])
    #print('focus_pair',focus_pair)
    correct = focus_pair[1]

    incorrect = []
    for pair in resource['pairs']:
        if pair[0]!=focus_pair[0]:
            if type(pair[1])in(tuple, list):
                incorrect+=list(pair[1])
            else:
                incorrect.append(pair[1])

    try:    
        for pair in resource['fillers']:
            if pair[0]!=focus_pair[0]:
                if type(pair[1])in(tuple, list):
                    incorrect+=list(pair[1])
                else:
                    incorrect.append(pair[1])
    except KeyError as e:
        print(e, 'No fillers, no worries!')
    #print(incorrect)

    posneg = randint(0,1)
    #print('posneg',posneg)
    if len(correct)!=3:#if we don't have three things which the correct answer is, we can't make the other type of question...
        posneg = 0

    try:#use special question if one exists
        raw_question=re.sub('POSNEG', resource['positive_negative'][posneg], resource['question_posneg'])
    except:#if not, go with the first pairs type question
        raw_question=re.sub('POSNEG', resource['positive_negative'][posneg], resource['question_with_0'])
    if posneg==1:
        correct, incorrect=incorrect, correct

    item_question_num = (0, 1) if posneg == 0 else (1, 0)#if 0,1 code goes into question, if 1,0 code is in items
    item_num, question_num = item_question_num[0], item_question_num[1]
    
    used = []
    id = 1
    items = []

    correct_item=choice(correct) 
    question_item=choice(focus_pair[0]) if type(focus_pair[0])in(list, tuple) else focus_pair[0]
    
    question_template = utl.raw_question_to_template_question(raw_question, question_item)
    #print('question_template',question_template)
    comment = False
    if item_num == 0:    
        items, id, used = utl.add_possible_code_item(correct_item, 'correct', items, id, used)
    else:
        if question_item[0] == '$':
            comment = True
            items.append({'code':'#' + correct_item, 'indicator':'correct', 'id':f'item{id}'})
        else:
            items.append({'item':correct_item, 'indicator':'correct', 'id':f'item{id}'})
        used.append(focus_pair[1])
        #id+= 1
    #print('pre items')
    items = utl.populate_items(incorrect, items, id, used, comment)
    #print('post items')
    shuffle(items)
    shuffle(items)
    return question_template, items