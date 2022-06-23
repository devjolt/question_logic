from random import choice, randint, shuffle
import re

from question_logic import utility_logic as utl


def logic(resource):

    '''Creates random question and item string for questions about correct order e.g.
    Question: What is the correct order to count in from lowest to highest:
    1. 1,2,3
    2. 3,2,4
    3. 1,2,9
    4. 3,2,1

    requires
    resource = {
        'question_order':'What best describes the killchain from PLACEHOLDER?',
        'ascending_descending':('first to last', 'last to first'),
        'type':['order_pairs'],
        'course_code':'',
        'pairs':[
            ('correct',['A','B','C','D']),
            ('incorrect',['1', '2', '3','4']),
            ('ambiguous',['0', '9', '8','7']),
            
        ],
        'fillers': (
            ('backwards',['z', 'y', 'x','w']),
        )
    }
    '''
    num_choices=4#number of options to present
    item_id=1
    #order= ascending_order if randint(0,1)==0 else descending_order
    asc_des=randint(0,1)
    
    #0 uses only the name part
    #1 uses only the description part  

    question_text=re.sub('PLACEHOLDER', resource['ascending_descending'][asc_des], resource['question_order'])
    
    question=[
        {'text':question_text}
    ]
    name_or_description = randint(0,1)#0 to use names, 1 to use descriptions
    correct_list=[]
    for item in resource['pairs']:
        if type(item[name_or_description])in(tuple, list):
            correct_list.append(choice(item[name_or_description]))
        else:
            correct_list.append(item[name_or_description])
        
    correct_str=', '.join(correct_list) if asc_des==0 else ', '.join(correct_list[::-1])
    used=[correct_str]
    items=[{'item':correct_str, 'indicator':'correct', 'id':'item1'}]

    fillers=[]
    for item in resource['fillers']:
        if type(item[name_or_description])in(tuple, list):
            fillers.append(choice(item[name_or_description]))
        else:
            fillers.append(item[name_or_description])
    
    all_options=correct_list+fillers
    while len(used)!=num_choices:
        shuffle(all_options)
        new_str=', '.join(all_options[-len(correct_list):])
        if new_str not in used:
            used.append(new_str)
            item_id+=1
            items.append({'item':new_str, 'indicator':'incorrect', 'id':f'item{item_id}'})
    shuffle(items)
    shuffle(items)
    return question, items