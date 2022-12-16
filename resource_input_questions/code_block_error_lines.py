from random import choice, randint, shuffle
import re

from question_logic import utility_logic as utl


"""Takes a list of correct statements and reverses them by negating or un-negating verbs to
make incorrect statements
"""

def logic(resource):
    """one data structure idea considered, but not worth the hastle

    # valid is a tuple containing tuples containing VALID lines of code, which would run without error to produce a desired outcome
    valid = (
        (
            (('line1a','line1b')'$comment for line'),# each line will be a valid line leading to the outcome described in comment
            (('line2a','line2b')'$comment for line'),# each line's comment assumes that the previous line of code has successfully run
            (('line3',)'$outcome of the whole block of code'), # final line's comment assumes the entire block runs successfully
        ),(
            (('altline1a','altline1b')'$altcomment for line'),
            (('altline2a','altline2b')'$altcomment for line'),
            (('altline3',)'$altoutcome of the whole block of code'),
        )
    )
    # note the commas in tuples with only one item, otherwise they're strings and this screws EVERYTHING up
    ONE of the above will be picked to be the valid code to be used in the question

    # invalid is also a tuple of tuples. Each tuple contains alternative outcome lines for ONE of the valid lines
    invalid = (
        (
            (('badline1a','badline1b')'$some error'),# each comment must describe behaviour for all lines in preceding tuple (in this case badline1a and badline1b both produce the same error)
            (('badline1c','badline1d')'$unexpected behaviour'),# assume that the rest of the code is normal when writing the comments
            (('badline1e',)'$another error'), # each comment describes the outcome of the code IF THIS WERE THE ONLY LINE CHANGED 
        ),
        (
            (('badline2a','badline2b')'$some error'),# 
            (('badline2c','badline2d')'$unexpected behaviour'),# 
            (('badline2e',)'$another error'), # 
        ),
        (
            (('badline3a','badline3b')'$some error'),# 
        ),
    )
    # in invalid, one tuple exists for each correct line of code. Each tuple contains alternatives for only one line

    3. select number of line of code which will cause x

    no matter what:
    # select which valid to use
    # compile all comments into one structure (list(set))
    # select whether question will be valid or invalid

    handle 3
    # if valid, correct answer will be none code completes successfully
    # incorrect answers will be random numbers from range of code length
    # code will be valid code

    #if invalid, corret answer will be index number selected from range of code length
    # incorrect answers will include code completes successfully plus two other unused index numbers
    # code will be valid code, with a corresponding incorrect line inserted in
    #NOTE: requires at least three lines of code...
    """
    # use default question text if not provided in resource
    text = 'Which line of code will cause the following snippet to fail:'
    text = resource['question'] if 'question' in resource else text
    
    # question should always be supplied with valid code, so handle that first
    code_valid = True
    valid = resource['valid']
    chosen_valid = choice(valid) # select which valid to use
            
    """
    try:
        lines_to_use = randint(3, len(chosen_valid)) # select the number of lines to use for question
    except Exception as e:
        print('Not enough options...', e)
        lines_to_use = 3
    
    lines_to_use = None if lines_to_use==len(chosen_valid) else lines_to_use
    """
    lines_to_use = None # use all lines
    selected_valid = chosen_valid[:lines_to_use] # rebuild valid and invalid based on number of lines to use

    comments = []
    for valid_code in valid:
        comments+= [comment[1] for comment in valid_code]

    if 'invalid' in resource: # if supplied with resource, do the same for invalid code
        invalid = resource['invalid']
    
        if len(valid[0]) != len(invalid): # check that invalid code has same number of lines as valid code
            print(f'Valid len ({len(valid[0])}) != invalid len ({len(invalid)})')
            # log error here:
            return None

        for line_group in invalid:
            comments+= [comment[1] for comment in line_group]

        selected_invalid = invalid[:lines_to_use]
        code_valid = True if randint(0,1)==0 else False

    # compile all comments into one structure (list(set))
    comments = list(set(comments))

    items, id, used = [], 1, []
    code = ''''''
    
    if code_valid is False:#the code will fail...
        print('Code will fail')
        invalid_index = randint(0, len(selected_valid[0])-1)#choose index of incorrect line
        print('invalid_index:',invalid_index)
        print('len:',len(selected_valid[0]))

        correct_invalid_items = invalid[invalid_index]#get all entries at that index
        print('correct_invalid_items:',correct_invalid_items)
        correct_invalid_line, _ = choice(correct_invalid_items)#get one entry from that
        correct_invalid_line = choice(correct_invalid_line) # pick one line

        items = []
        items.append({'item':invalid_index+1, 'indicator':'correct', 'id':f'item{id}'})#use a correct answer
        id+=1#increment id
        used = [invalid_index+1]
        
        items.append({'item':'The code will execute successfully', 'indicator':'incorrect', 'id':f'item{id}'})#use a correct answer
        id+=1#increment id
        

        nums = [i for i in range(len(selected_valid))]
        
        print(used, nums)
        while len(items) != 4:
            num = choice(nums) +1
            #print(num, used)
            if num not in used:
                items.append({'item':num, 'indicator':'incorrect', 'id':f'item{id}'})
                used.append(num)
                id+=1

        #build a string with all but failing line correct
        for i in range(len(selected_valid)):
            if i == invalid_index:
                print('correct_invalid_line:',correct_invalid_line)
                code+= correct_invalid_line + '\n'
            else:
                valid_line = selected_valid[i]#first item in valid[i] tuple
                code+= choice(valid_line[0]) + '\n'

    else:#the code will actually not fail
        print('Code runs OK')
        items.append({'item':'The code will execute successfully', 'indicator':'correct', 'id':f'item{id}'})
        id+=1

        nums = [i for i in range(0, len(selected_valid))]
        print('selected_valid:',selected_valid)
        shuffle(nums)    
        
        for num in nums[:3]:
            items.append({'item':num+1, 'indicator':'correct', 'id':f'item{id}'})
            used.append(num+1)
            id+=1

        for line in selected_valid:
            print('line:',line)
            code+= choice(line[0]) + '\n'
    
    question=[
        {'text':text}, 
        {'code':code}
    ]
    return question, items
