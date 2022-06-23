from random import choice, randint, shuffle
import re

from question_logic import utility_logic as utl


def logic(resource):
    # if correct = an error
    # select an error line number
    # every line up to error line is correct
    # every line after error line can be correct or incorrect
    # incorrect answers can be any other number than that of the correct line or "there is no error"
    # if correct = there is no error:
    # one of each valid lines
    # incorrect is one of each random lines
    valid, invalid = resource['valid'], resource['invalid']
    question = [{'text':'Which line will cause this code to fail?'}]
    code=''''''
    used,items, id=[],[], 1
    if randint(0, 1) == 0:#the code will fail...
        #pick which line will cause failure
        error_line = randint(0, len(valid)-1)
        
        items.append({'item':error_line+1, 'indicator':'correct', 'id':f'item{id}'})
        id+=1
        if randint(0,1) == 0:#chance for statement that the code will run without error
            used.append('No failure')
            items.append({'item':'The code will execute successfully', 'indicator':'incorrect', 'id':f'item{id}'})
            id+=1
        while len(used) != 3:
            num = randint(0, len(valid)-1)
            if num != error_line:
                used.append(num)
                used = list(set(used))
                print(used)
        for num in used:
            if num != 'No failure':
                items.append({'item': num+1, 'indicator':'incorrect', 'id':f'item{id}'})
                id+=1
        #build a string with all but failing line correct
        for i in range(len(valid)):
            if i == error_line:
                code+= utl.pick_one_many_times(choice(invalid[i])[0]) + '\n'
            else: 
                code+= utl.pick_one_many_times(choice(valid[i])[0]) + '\n'
    else:#the code will actually not fail
        items.append({'item':'The code will execute successfully', 'indicator':'correct', 'id':f'item{id}'})
        id+=1
        while len(used) != 3:
            num = randint(0, len(valid)-1)
            if num not in used:
                item = num+1
                items.append({'item':num+1, 'indicator':'incorrect', 'id':f'item{id}'})
                id+=1
                used.append(item)
        for line in valid:
            code+= utl.pick_one_many_times(choice(line)[0]) + '\n'
    question.append({'code':code})
    shuffle(items)
    return question, items