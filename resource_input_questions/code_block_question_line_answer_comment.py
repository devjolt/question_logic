from random import choice, randint, shuffle
import re

from question_logic import utility_logic as utl

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
    NOTE: NO COMMENT = Count as a line, but ignore as a correct line?

    # collect all comments
    # decide on either valid or invalid code. 
    # select focus_line_index+1

    # if valid_code:
    # if correct:
    # do_not_use = valid focus_index
    # correct = an accurate comment is not present
    # else:   
    # correct = focus_line comment
    # make all valid code

    # if invalid code:
    # if correct:
    # if focus_line_index > fail_line_index:
    # correct = irrelevant because code has previously failed
    # elif focus_line_index == fail_line_index:
    # correct = invalid focus line index comment
    # else:
    # correct = valid focus line index comment
        
    # else:
    # do_not_use = invalid focus_index
    # correct = an accurate comment is not present
    
    # select failure line use correct code up to the failure line and either correct or incorrect code thereafter

    # if not in used add irrelevant because code has previously failed
    # while len(items) is not 4:
    # pick random item from comments:
    # if item not in used
    # try:
    # if item!= do_not_use
    # add_item
    # except: 
    # add_item

    # question = which comment best matches line focus_line_index+1

    """
    # question should always be supplied with valid code, so handle that first
    valid = resource['valid']

    comments = []
    for valid_code in valid:
        comments+= [comment[1] for comment in valid_code]

    chosen_valid = choice(valid) # select which valid to use
    
    try:
        lines_to_use = randint(3, len(chosen_valid)) # select the number of lines to use for question, minimum of 3
    except Exception as e:
        print('Not enough options...', e)
        lines_to_use = 3

    lines_to_use = None if lines_to_use == len(chosen_valid) else None
    
    selected_valid = chosen_valid[:lines_to_use] # rebuild valid and invalid based on number of lines to use

    focus_line_index = randint(0, len(selected_valid)-1) # select which line to use in question
    print('focus_line_index:',focus_line_index)

    text = f'Which comment best matches line {focus_line_index+1}:'
    
    if 'question' in resource: # if custom question supplied, use it
        text = re.sub('PLACEHOLDER', str(focus_line_index+1), resource['question'])
     
    code_valid = True # default value
    
    if 'invalid' in resource: # if supplied with resource, do the same for invalid code
        invalid = resource['invalid']

        for line_group in invalid:
            comments+= [comment[1] for comment in line_group]

        if len(valid[0]) != len(invalid): # check that invalid code has same number of lines as valid code
            print(f'Valid len ({len(valid[0])}) != invalid len ({len(invalid)})')
            # log error here:
            return None
        
        #selected_invalid = selected_valid[:lines_to_use] # this block if we want to use a random number of lines in this question
        selected_invalid = invalid

        code_valid = True if randint(0,1)==0 else False

    # compile all comments into one structure (list(set))
    comments = list(set(comments))

    code = ''''''
    do_not_use = False

    correct_options = True if randint(0,2)==1 else False

    accurate_comment_not_present = '# an accurate comment is not present'
    irrelevant_previous_failure = '# irrelevant because previous lines have already failed'
    constant_answers_list = [accurate_comment_not_present]

    # start handling valid and invalid
    if code_valid is True:
        if correct_options is True:
            correct = selected_valid[focus_line_index][1]
        else:
            do_not_use = selected_valid[focus_line_index][1]
            correct = accurate_comment_not_present
        
        for line in selected_valid:
            code+= choice(line[0]) + '\n'
    
    elif code_valid is False:

        fail_line_index = randint(0, len(selected_invalid)-1)
        fail_line = choice(selected_invalid[fail_line_index])
        print('correct_options:',correct_options)
        if focus_line_index<fail_line_index:
            correct = selected_valid[focus_line_index][1]
            print('valid fail_line_index:',fail_line_index)
        elif fail_line_index == focus_line_index:
            correct = fail_line[1]
            print('invalid : failed this line: fail_line_index:',fail_line_index)
        elif fail_line_index<focus_line_index:
            correct = irrelevant_previous_failure
            print('invalid: failed because of previous failure fail_line_index:',fail_line_index)

        if correct_options is False:
            constant_answers_list.append(irrelevant_previous_failure)
            do_not_use = correct
            correct = accurate_comment_not_present
        
        for i in range(0, len(selected_valid)):
            if i<fail_line_index: # line is valid
                to_add = choice(selected_valid[i][0]) + '\n' 
                
            elif i==fail_line_index: # line is invalid
                to_add = choice(fail_line[0]) + '\n'
                
            elif fail_line_index<i:
                
                if randint(0,1)==0: # line can be either valid or valid
                    to_add = choice(choice(selected_invalid[i])[0]) + '\n'

                else:
                    to_add = choice(valid_code[i][0]) + '\n'

            code+= to_add

    """
    if 'constants' in resource:
        for name_space in resource['constants'].keys():
            code = re.sub(name_space, resource['constants'][name_space], code)
    """
    if 'constant_collections' in resource:
        # select a collection
        collections = resource['constant_collections']
        collection_selection = collections[choice(list(resource['constant_collections'].keys()))]
        for name_space in collection_selection.keys():
            code = re.sub(name_space, collection_selection[name_space], code)
    
    # fill items
    id, used = 1, []
    items = [{'code':correct, 'indicator':'correct', 'id':f'item{id}'}]
    used = [correct, do_not_use]
    id+=1

    # add any un-added items
    for attempt in constant_answers_list:
        
        if attempt not in used:
            items.append({'code':attempt, 'indicator':'incorrect', 'id':f'item{id}'})
            used.append(attempt)
            id+=1

    while len(items)!=4: # fill with other random items
        attempt = choice(comments)#pick a comment
        if attempt not in used:
            items.append({'code':attempt, 'indicator':'incorrect', 'id':f'item{id}'})#use a correct answer
            used.append(attempt)
            id+=1

    question=[
        {'text':text}, 
        {'code':code}
    ]
    shuffle(items)
    return question, items