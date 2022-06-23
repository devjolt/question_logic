from random import choice, randint, shuffle
import re

from question_logic import utility_logic as utl


def logic(resource):

    # if outcome is run successfully
    # pick one of each correct lines and correct answer is comment from final line
    # elif fail, 
    # pick line of failure, along with correct answer: comment (reason for failure)
    # every line up to failure line must be valid
    # lines after incorrect line can be valid or invalid
    # one incorrect answer is comment from successful final line
    # other incorrect answers are random incorrect answers from other lines if different to correct answer

    valid, invalid = resource['valid'], resource['invalid']
    question = [{'text':'What is the outcome of the following code?'}]
    code=''''''
    used,items, id=[],[], 1

    # Check that length of valid and invalid are the same
    if len(valid) != len(invalid):
        print(f'Valid len ({len(valid[0])}) != invalid len ({len(invalid)})')
        return None
    
    # Choose between one incorrect vs all correct
    if randint(0,3) in [0,1,2]:#one incorrect
        #print('incorrect')
        invalid_index = randint(0, len(valid)-1) # Choose index of incorrect line   
        choice_index = randint(0, len(valid[invalid_index])-1)
        #print(invalid_index+1, choice_index+1)
        #print(invalid[invalid_index][choice_index])

        items.append({'code':invalid[invalid_index][choice_index][1], 'indicator':'correct', 'id':f'item{id}'})
        used.append(invalid[invalid_index][choice_index][1])
        id+=1 # Increment id

        # Incorrect item: code outcome successful
        items.append({'code':choice(valid[-1]), 'indicator':'incorrect', 'id':f'item{id}'})
        id+=1 # Increment id

        # Select two other invalid outcomes NOT THE SAME AS THE correct answer
        while len(used)!=3:
            
            # Select another invalid answer NOT matching index of correct_answer
            attempt = utl.pick_one_many_times(invalid)[1]
            if attempt not in used:
                items.append({'code':attempt, 'indicator':'incorrect', 'id':f'item{id}'})
                used.append(attempt)
                id+=1 # Increment id

        # Build code string
        for i in range(len(valid)):
            if i < invalid_index:
                code+= utl.pick_one_many_times(choice(valid[i])[0]) + '\n'
            elif i == invalid_index:
                code+= invalid[invalid_index][choice_index][0] + '\n'
            else:
                if randint(0,1)==0:
                    code+= utl.pick_one_many_times(choice(valid[i])[0]) + '\n'
                else:
                    code+= utl.pick_one_many_times(choice(invalid[i])[0]) + '\n'
                
    else:#all correct
        #print('all correct')
        valid_code_index = randint(0, len(valid[-1])-1)
        items.append({'item':valid[-1][valid_code_index][1], 'indicator':'correct', 'id':f'item{id}'})#use a correct answer
        id+=1#increment id
        #select three random unique incorrect answers
        while len(used)!=3:
            line = choice(invalid)#pick a line
            attempt = choice(line)[1]
            if attempt not in used:
                items.append({'code':attempt, 'indicator':'incorrect', 'id':f'item{id}'})
                id+=1
                used.append(attempt)
        for line in valid:
            code+= utl.pick_one_many_times(choice(line)[0]) + '\n'
    question.append({'code':code})
    shuffle(items)
    return question, items