import os
from pathlib import Path

try:
    resource_input_questions_folder = Path('./question_logic/resource_input_questions/')
    resource_dir = list(os.listdir(resource_input_questions_folder))

except FileNotFoundError:
    resource_input_questions_folder = Path('mysite/question_logic/resource_input_questions/')
    resource_dir = list(os.listdir(resource_input_questions_folder))

for item in resource_dir:
    if item not in ['__init__.py', 'utility_logic.py', '__pycache__']:
        #print('asdf',item)
        exec(f'from .resource_input_questions import {item[:-3]}')

