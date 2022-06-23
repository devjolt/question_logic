from random import choice, randint, shuffle
import re

from question_logic import utility_logic as utl

def logic(resource):
    """
resource = {
    'type':'auto_correct_incorrect',
    'verbs':(),
    'negator':'not',
    'correct':(
        'i can eat',
        'i will game',
        'i can not sleep',
        'i may not stop'
        )
    }
    """
    item_id = 1
    negator = resource['negator']
    verbs = resource['verbs']
    if randint(0,1) == 0:
        question = 'Which of the following is correct?'
        # Pick correct answer
        correct = choice(resource['correct'])
        
        items=[{
            'item':correct,
            'indicator':'correct',
            'id':f'item{item_id}'
            }]
        used = [correct]

        while len(items)!=4:
            item = choice(resource['correct'])
            if negator in item:# remove negator and move on
                item = re.sub(f"{negator} ", '', item)
            else:# add negator after a verb
                for word in verbs:
                    if word in item:
                        _, end = re.search(word, item).span(0)
                        item = item[:end] + f' {negator}' + item[end:]
                    break
            
            if item not in used:
                item_id+=1
                items.append({
                    'item':item,
                    'indicator':'incorrect',
                    'id':f'item{item_id}'
                    })
                used.append(item)

    else:
        question = 'Which of the following is incorrect?'
        # Pick correct answer
        correct = choice(resource['correct'])
        if negator in correct:# remove negator and move on
            correct = re.sub(f"{negator} ", '', correct)
        else:# add negator after a verb
            for word in verbs:
                if word in correct:
                    _, end = re.search(word, correct).span(0)
                    correct = correct[:end] + f' {negator}' + correct[end:]
                    break
        
        items=[{
            'item':correct,
            'indicator':'correct',
            'id':f'item{item_id}'
            }]
        used = [correct]

        while len(items)!=4:
            item = choice(resource['correct'])
            
            if item not in used:
                item_id+=1
                items.append({
                    'item':item,
                    'indicator':'incorrect',
                    'id':f'item{item_id}'
                    })
                used.append(item)
    shuffle(items)
    return [{'text':question}], items