from random import choice, randint, shuffle
import re

from question_logic import utility_logic as utl

"""Creates a multi option question from a list of correct and incorrect statements
"""

def logic(resource):
    #choose whether right answers are correct or incorrect
    if randint(0,1)==0:
        right, wrong = (resource['positive'],resource['correct']), (resource['negative'],resource['incorrect'])
    else:
        right, wrong = (resource['negative'],resource['incorrect']), (resource['positive'],resource['correct'])  
    first_question_part = re.sub('PLACEHOLDER', right[0], resource['question'])
    first_question_part=re.sub(' is ', ' are ', first_question_part)
    right, wrong = list(right[1]), list(wrong[1])
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
        
    items, id, used = utl.add_possible_code_item(correct, 'correct', [], 1, [])

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
            items, id, used = utl.add_possible_code_item(incorrect, 'incorrect', items, id, used)#item, indicator, items, id, used,
        else:
            continue
    shuffle(items)
    shuffle(items)
    return question, items