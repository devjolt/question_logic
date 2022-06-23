from random import choice, randint, shuffle
import re

from question_logic import utility_logic as utl


def logic(resource):

    # if correct = there is no error:
    # one of each valid lines
    # incorrect is one of each random lines

    # if correct = an error line
    # select an error line number and comment to include in the question
    # other lines chosen at random, as long as they don't have the same comment as correct answer
    
    valid, invalid = resource['valid'], resource['invalid']
    question = [{'text':'Which line will cause this code to fail with the following error:'}]
    code=''''''
    used,items, id=[],[], 1
    if randint(0, 1) == 0:#the code will fail...
        print('fail')
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
            if i < error_line:
                code+= utl.pick_one_many_times(choice(valid[i])[0]) + '\n'
            elif i == error_line:
                line = choice(invalid[i])
                comment = f'# Fails with {line[1]}\n\n'
                code+= line[0] + '\n'
            else: 
                if randint(0,1)==0:
                    code+= utl.pick_one_many_times(choice(valid[i])[0]) + '\n'    
                else:
                    code+= utl.pick_one_many_times(choice(invalid[i])[0]) + '\n'
    else:#the code will actually not fail
        print('succeed')
        items.append({'item':'The code will execute successfully', 'indicator':'correct', 'id':f'item{id}'})
        id+=1
        comment = f'# fails with {utl.pick_one_many_times(invalid, 2)[0]}\n\n'
        while len(used) != 3:
            num = randint(0, len(valid)-1)
            if num not in used:
                item = num+1
                items.append({'item':num+1, 'indicator':'incorrect', 'id':f'item{id}'})
                id+=1
                used.append(item)
        for line in valid:
            code+= utl.pick_one_many_times(choice(line)[0]) + '\n'
            comment = f'# Fails with {choice(choice(invalid))[1]}\n\n'
    question.append({'code':comment})
    question.append({'code':code})
    shuffle(items)
    return question, items
