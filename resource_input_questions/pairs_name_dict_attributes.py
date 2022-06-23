from random import choice, randint, shuffle
import re

from question_logic import utility_logic as utl

def logic(resource:dict):
    """Create a question with a resource containing name attribute pairs as follows:

'question_with_name':'Which best describes an AWS PLACEHOLDER?',
'question_with_attribute':'Which member of the Snow family is described by the following: PLACEHOLDER',
'type':'name_attribute',
'name_attribute_pairs':(
    ('Snowcone',{'description':'a small, rugged, and secure edge computing and data transfer device', 'CPUs':'2 CPUs', 'memory':'4 GB memory', 'storage':'8 TB storage'}),
    ('Snowball Edge Storage Optimised ',{'description':['well suited for large-scale data migrations and recurring transfer workflows', 'well suited for local computing with higher capacity needs'], 'CPUs':'40 vCPUs', 'memory':'80 GiB memory', 'storage':'80 TB HDD for S3 compatible storage and 1 TB SSD for block volumes'}),
    ('Snowball Edge Compute Optimised ',{'description':'provides powerful computing resources for use cases such as machine learning, full motion video analysis, analytics, and local computing stacks', 'CPUs':['52 vCPUs', 'optional NVIDIA Tesla V100 GPU'], 'memory':'208 GiB memory', 'storage':'42 TB HDD for S3 compatible storage and 7.68 TB SDD for block volumes'}),
    ('Snowmobile',{'description':['an exabyte-scale data transfer service used to move large amounts of data to AWS', 'a 45-foot long ruggedized shipping container, pulled by a semi trailer truck'], 'CPUs':'Number of CPUs not applicable', 'memory':'memory not applicable', 'storage':'100 petabytes'}),
),
'fillers':(
    (['Snowboard', 'Snowman', 'Icecream', 'Glacier', 'SnowPop'],{'description':['a high capacity EC2 instance', 'an AWS laptop connected to the cloud',], 'CPUs':f"{choice([4, 6, 8, 100])} {choice(['CPUs', 'vCPUs'])}", 'memory':f"{choice(['2 GB', '6 GB', '8 GB', '40 GiB', '42 GiB', '50 GiB'])} memory", 'storage':[f"{randint(10, 100)} {choice(['GB', 'GiB', 'TB'])} HDD for S3 compatible storage and {randint(1, 10)} {choice(['GB', 'GiB', 'TB'])} SSD for block volumes", f"{randint(10, 100)} {choice(['GB', 'GiB', 'TB'])} storage"]}),
)

Functionality
-------------
# Select a subject name, attribute set and focus attribute
# Choose between question with name and question with attribute
# if question with name:
# substitute name into question
# Get correct answer using correct attribute
# Get three other incorrect answers using incorrect attributes
# if question with attribute:
# Get correct answer from subject name
# Get three other incorrect answers using incorrect names
    """
    pairs = list(resource['name_attribute_pairs'])
    shuffle(pairs)
    
    # Select a subject name, attribute set and focus attribute
    correct_line = pairs.pop()
    correct_name, correct_attributes = correct_line
    focus_attribute = choice(tuple(correct_attributes.keys()))

    # Create incorrect list by adding fillers
    pairs+=list(resource['fillers'])

    # Choose between question with name and question with attribute
    if randint(0,1) == 0: # if question with name

        # substitute name into question
        question = re.sub(
            'PLACEHOLDER',
            utl.pick_one_many_times(correct_name),
            resource['question_with_name']
            )

        # Get correct answer using correct attribute
        item_id = 1
        item = correct_attributes[focus_attribute]
        item = utl.pick_one_many_times(item)
        
        items=[{
            'item':item,
            'indicator':'correct',
            'id':f'item{item_id}'
            }]
        used = [item]

        # Get three other incorrect answers using incorrect attributes
        while len(items)!=4:
            item = choice(pairs)[1][focus_attribute]
            item = utl.pick_one_many_times(item)
            
            if item not in used:
                item_id+=1
                items.append({
                    'item':item,
                    'indicator':'incorrect',
                    'id':f'item{item_id}'
                    })
                used.append(item)
    
    else:# if question with attribute:
        # substitute attrubute into question
        question = re.sub(
            'PLACEHOLDER',
            utl.pick_one_many_times(correct_attributes[focus_attribute]),
            resource['question_with_attribute']
            )
    
        # Get correct answer from subject name
        item_id = 1
        item = utl.pick_one_many_times(correct_name)
        items=[{
            'item':item,
            'indicator':'correct',
            'id':f'item{item_id}'
            }]
        used = [item]
        
        # Get three other incorrect answers using incorrect names
        while len(items)!=4:
            item = utl.pick_one_many_times(choice(pairs)[0])
            if item not in used:
                item_id+=1
                items.append({
                    'item':item,
                    'indicator':'incorrect',
                    'id':f'item{item_id}'
                    })
                used.append(item)

    shuffle(items)
    return [{'text':question}], items