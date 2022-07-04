from random import choice, randint, shuffle
import re

from question_logic import utility_logic as utl

"""can be used to make something like a correct/incorrect question from groups of pairs.
Works as long as each pair has at least 4 items. 
"""

def logic(resource):
    '''
    resource = {
        'question_with_0':'Which isPOSNEG an example of PLACEHOLDER?',
        'positive_negative':('',' not'),
        'type':['multi_option_pairs'],
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
    #select a 'right' row
    right_row = choice(resource['pairs'])
    posneg=randint(0,1)
    
    question_item=0
    answer_item=1
    
    try:
        first_question_part = re.sub('POSNEG', resource['positive_negative'][posneg], resource['question_with_0'])
    except:
        first_question_part = re.sub('POSNEG', resource['positive_negative'][posneg], resource['question_posneg'])

    #different to multi_from_correct_incorrect because no need to have positive and negative at this stage    
    try:
        first_question_part = re.sub('PLACEHOLDER', right_row[question_item], first_question_part)
    except:
        first_question_part = re.sub('PLACEHOLDER', choice(right_row[question_item]), first_question_part)        
    first_question_part = re.sub(' is ', ' are ', first_question_part)


    if type(right_row[answer_item]) in (list,tuple):
        right=right_row[answer_item]
    else:
        right=[right_row[answer_item]]

    wrong=[]
    for row in resource['pairs']:
        if row[0]!=right_row[0]:
            if type(row[answer_item])in(list, tuple):
                wrong+=row[answer_item]
            else:
                wrong+=[row[answer_item]]
    try:
        for row in resource['fillers']:
            if type(row[answer_item])in(list, tuple):
                wrong+=list(row)
            else:
                wrong+=[row[answer_item]]
    except KeyError as e:
        print(e, 'No fillers, no worries!')
    if posneg==1:
        right, wrong=wrong, right
    
    #following code identical to other pairs stuff...
    
    shuffle(wrong)#randomise order of both
    shuffle(right)
    #make first part of question
    
    question = [{'text':first_question_part}]
    #choose number of right answers
    
    max_right=4
    number_right = randint(0, max_right)
    letters_list = ['a', 'b', 'c', 'd']
    building_items_letters_list=['a', 'b', 'c', 'd']
    #print('number right',number_right)
    #print('question', question)
    #print('right', right)
    #print('wrong', wrong)
    for i in range(2):
        changes_made=0
        #note there must be enough right and wrong answers for this  to work... loop checks this!
        if len(wrong)<4-number_right:#if less wrong answers available than we need
            number_right=max_right-len(wrong)#use max number of wrong answers by altering number_right
            changes_made+=1

        if len(right)<number_right:#if less right answers available than we need
            number_right=len(right)#use max number of right answers by altering number_right
            changes_made+=1

        #print(changes_made)
        if changes_made==2:#if we've changed both, then it is impossible to create this question because it doesn't have enough right or wrong answers
            if i == 1:#If this is the case on the second time around, question building is doomed to fail when popping answers below
                print('Error: question resource does not have enough right or wrong answers!')      
                break
            max_right=3#try reducing the number of letters available and try again...
            number_right = randint(0, max_right)
            letters_list = ['a', 'b', 'c']
            building_items_letters_list=['a', 'b', 'c']
            continue
        
        break

    #print('max_right:', max_right)

    if number_right==0:
        wrong_answers=wrong[0:max_right-number_right]
        #print('wrong answers:', wrong_answers)
        correct='none of the above'
        for i in range(number_right+len(letters_list)):
            question.append({'text':f'{letters_list[i]}. {wrong_answers[i]}'})
    elif number_right==max_right:
        correct='all of the above'
        right_answers=right[0:max_right]
        for i in range(max_right):
            question.append({'text':f'{letters_list[i]}. {right_answers[i]}'})
    else:
        letters_dict = {'a':None, 'b':None, 'c':None, 'd':None}
        right_letters, wrong_letters=[], []
        right_answers=right[:number_right]
        wrong_answers=wrong[0:max_right-number_right]
        shuffle(letters_list)
        for i in range(len(right_answers)):
            #print('right letters:', letters_list)
            #print('right answers:', right_answers)
            letter=letters_list.pop()
            letters_dict[letter]=right_answers[i]
            right_letters.append(letter)
        while len(letters_list)!=0:
            #print('wrong letters:', letters_list)
            #print('wrong answers:', wrong_answers)
            letter=letters_list.pop()
            letters_dict[letter]=wrong_answers.pop()
            wrong_letters.append(letter)
        right_letters.sort()
        correct=', '.join(right_letters)
        for letter in building_items_letters_list:
            question.append({'text':f'{letter}. {letters_dict[letter]}'})
    item_id=1
    items=[{'item':correct, 'indicator':'correct', 'id':f'item{item_id}'}]
    used=[correct]

    #make incorrect answers
    while len(items)!=4:#we want there to be four items
        
        number = randint(0, max_right)#pick type of wrong answer using max_right (usually 4, 3 if inadequate numbers of right or wrong answers)
        if number==0:
            incorrect='none of the above'
        elif number==max_right:
            incorrect='all of the above'
        else:
            letters=building_items_letters_list
            shuffle(letters)
            letters = letters[0:number]
            letters.sort()
            incorrect=', '.join(letters)
        if incorrect not in used:
            item_id+=1
            items.append({'item':incorrect, 'indicator':'incorrect', 'id':f'item{item_id}'})
            used.append(incorrect)
        else:
            continue
    shuffle(items)
    shuffle(items)
    return question, items