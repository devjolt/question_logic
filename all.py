import os
from pathlib import Path
import platform

if platform.system() == 'Windows':
    resource_input_questions_folder = Path('./question_logic/resource_input_questions')
else:
    resource_input_questions_folder = Path('mysite/question_logic/resource_input_questions/')

for item in os.listdir(resource_input_questions_folder):
    if item not in ['__init__.py', 'utility_logic.py', '__pycache__']:
        #print('asdf',item)
        exec(f'from .resource_input_questions import {item[:-3]}')

