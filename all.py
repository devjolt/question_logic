import os

for item in os.listdir('.\\question_logic\\resource_input_questions'):
    if item not in ['__init__.py', 'utility_logic.py', '__pycache__']:
        #print('asdf',item)
        exec(f'from .resource_input_questions import {item[:-3]}')

