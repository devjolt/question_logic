from random import randint, choice
import re

def pick_one_many_times(item, depth = None):
    if depth is None:
        while True:
            if type(item) not in [tuple, list]:
                return item
            else:
                item=choice(item)
    else:
        for i in range(depth):
            item = choice(item)
        return item


def pick_one_from_nested(item, depth = None):
    if depth is None:
        while True:
            if type(item) not in [tuple, list]:
                return item
            else:
                item=choice(item)
    else:
        for i in range(depth):
            item = choice(item)
        return item

def raw_question_to_template_question(raw_question, placeholder_str):
    """Either way, placeholders need to be replaced as they appear...
    if raw_question is...
    - a string: assign one item as text and replace placeholder
    - a list of strings: for each item, replace placeholder, then assign each item as either text or code
    """
    template_question = []
    if type(raw_question) is str:#assume that strings will never just be pure code... I can't think why they would ever be
        template_question.append({'text':raw_question.replace('PLACEHOLDER', placeholder_str)})
    else:
        for line in raw_question:
            #replace PLACEHOLDER
            replaced_question = line.replace('PLACEHOLDER', placeholder_str)
            if replaced_question[0] != '$':
                template_question.append({'text':replaced_question})
            else:
                template_question.append({'code':replaced_question[1:]})
    return template_question

def add_item(item, indicator, items, id, used):
    """add item to items and used list
    """
    items.append({'item':item, 'indicator':indicator, 'id':f'item{id}'})
    id+=1
    used.append(item)
    return items, id, used
    
def add_possible_code_item(item, indicator, items, id, used, comment = False):
    #print('adding possible code item:', id, item)
    items = list(items)
    if item[0] == '$':
        print('code item:',item)
        items.append({'code':item[1:], 'indicator':indicator, 'id':f'item{id}'})
    else:
        if comment != True:
            items.append({'item': item, 'indicator':indicator, 'id':f'item{id}'})
        else:
            items.append({'code':'#' + item, 'indicator':indicator, 'id':f'item{id}'})
    id+=1
    used.append(item)
    #print(item)
    return items, id, used

def populate_items(incorrect, items, id, used, comment = False):
    while len(items) != 4:
        item = pick_one_many_times(incorrect)
        if item not in used:
            items, id, used = add_possible_code_item(item, 'incorrect', items, id, used, comment)   
    return items

def correct_incorrect_helper(correct, incorrect):         
    used = []
    items = []
    correct_item = choice(correct)
    items, id, used = add_possible_code_item(correct_item, 'correct', items, 1, used)
    items = populate_items(incorrect, items, id, used)
    return items

def add_code_line(line, code):
    line= choice(line)
    code+= line + '\n'
    return code

def add_constants_to_question_items(question, items, resource):
    collections = resource['constant_collections']
    # select a collection to use for this question
    constants = collections[choice(list(collections.keys()))] 
    for name_space in constants.keys(): # for each namespace in collection
        for line in question:
            if 'text' in line:
                line['text'] = re.sub(name_space, constants[name_space], line['text'])
            elif 'code' in line:
                line['code'] = re.sub(name_space, constants[name_space], line['code'])
            
        for item in items: # swap into items whether code or text
            try:
                if 'item' in item:
                    item['item'] = re.sub(name_space, constants[name_space], item['item'])
                elif 'code' in item:
                    item['code'] = re.sub(name_space, constants[name_space], item['code'])
            except TypeError as e:
                print('item is not a str')
            
    return question, items