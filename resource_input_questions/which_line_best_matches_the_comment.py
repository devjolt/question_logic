from random import choice, randint, shuffle
import re

from question_logic import utility_logic as utl


def logic(resource):


    # if question will contain the comment
    # pick one comment with line as correct answers
    # pick any three other lines as incorrect answers
    # elif question will contain the line
    # pick any line as correct answer and use comment in question
    # pick any three lines with other comments as incorrect answers

    all_items = resource['valid'] + resource['invalid']
    used,items, id=[],[], 1
    chosen = utl.pick_one_many_times(all_items, 2)
    used = [chosen[1]]
    if randint(0,1):
        question = [
            {'text':'Which line of code matches the following comment:'},
            {'code':f'# {chosen[1]}'}
        ]
        items = [{'code':utl.pick_one_many_times(chosen[0]), 'indicator':'correct', 'id':f'item{id}'}]
        id+=1
        while len(used) != 4:
            attempt = pick_one_many_times(all_items, 2)
            if attempt[1] not in used:
                items.append({'code':utl.pick_one_many_times(attempt[0]), 'indicator':'incorrect', 'id':f'item{id}'})
                used.append(attempt[1])
                id+=1
    else:
        question = [
            {'text':'Which comment matches the following line of code:'},
            {'code':f'{utl.pick_one_many_times(chosen[0])}'}
        ]
        items = [{'code':'# '+chosen[1], 'indicator':'correct', 'id':f'item{id}'}]
        id+=1
        while len(used) != 4:
            attempt = pick_one_many_times(all_items, 2)
            if attempt[1] not in used:
                items.append({'code':'# '+attempt[1], 'indicator':'incorrect', 'id':f'item{id}'})
                used.append(attempt[1])
                id+=1
        
    shuffle(items)
    return question, items
