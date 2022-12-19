from random import choice, randint, shuffle
import re

from question_logic import utility_logic as utl

def logic(resource):
    # note, this does not work if errors are NameEerrors. 
    # how are you going to tell if an arbitrarily 
    # named variable is incorrect?

    # if which random line is valid:
    # pick a valid line and use as correct answer
    # pick three other random invalid liness as incorrect answers
    # elif which random line is invalid:
    # pick an invalid line and use as correct answer
    # pick three other random valid lines as incorrect answers

    valid, invalid = resource['valid'], resource['invalid'] # get valid and invalid lines
    # isolate valid and invalid lines...


    used,items, id=[],[], 1
    if randint(0,1):
        
        correct = utl.pick_one_many_times(utl.pick_one_many_times(invalid, 2)[0])
        correct = re.sub('\t','', correct)
        question = [{'text':'Which line of code may not be invalid?'}]
        items = [{'code':correct, 'indicator':'correct', 'id':f'item{id}'}]
        used = [correct]
        id+=1
        while len(used) != 4:
            attempt = utl.pick_one_many_times(utl.pick_one_many_times(valid, 2)[0])
            attempt = re.sub('\t','', attempt)
            if attempt not in used:
                items.append({'code':attempt, 'indicator':'incorrect', 'id':f'item{id}'})
                used.append(attempt)
                id+=1
    else: 
        correct = utl.pick_one_many_times(utl.pick_one_many_times(valid, 2)[0])
        correct = re.sub('\t','', correct)
        question = [{'text':'Which line of code could be valid?'}]
        items = [{'code':correct, 'indicator':'correct', 'id':f'item{id}'}]
        used = [correct]
        id+=1
        while len(used) != 4:
            attempt = utl.pick_one_many_times(utl.pick_one_many_times(invalid, 2)[0])
            attempt = re.sub('\t','', attempt)
            if attempt not in used:
                items.append({'code':attempt, 'indicator':'incorrect', 'id':f'item{id}'})
                used.append(attempt)
                id+=1
    shuffle(items)

    if 'constant_collections' in resource: # if this has been passed into resource...
        question, items = utl.add_constants_to_question_items(question, items, resource)#

    return question, items
