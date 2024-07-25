from SpecializedModel import *
import pandas as pd
import time
import csv 
from sys import argv
import re

df = pd.read_csv(argv[2], delimiter=";", header=0)

def Convert_to_lst(str_lst): 
    str_lst = str_lst[1:-1]
    li = str_lst.split(", ")
    return li 

# Define a dictionary to map class names to their corresponding classes
class_map = {
    'Choice': Choice,
    'ExclusiveChoice': ExclusiveChoice,
    'End': End,
    'Init': Init,
    'Existence': Existence,
    'Exactly': Exactly,
    'RespondedExistence': RespondedExistence,
    'CoExistence': CoExistence,
    'Response': Response,
    'Precedence': Precedence,
    'Succession': Succession,
    'AlternateResponse': AlternateResponse,
    'AlternatePrecedence': AlternatePrecedence,
    'AlternateSuccession': AlternateSuccession,
    'ChainResponse': ChainResponse,
    'ChainPrecedence': ChainPrecedence,
    'ChainSuccession': ChainSuccession,
    'NotCoExistence': NotCoExistence,
    'NotSuccession': NotSuccession,
    'NotChainSuccession': NotChainSuccession,
    'Absence': Absence
}

# Function to transform string into Constraint instance
def transform_item(item):
    # match = re.match(r'(\w+)\((\w+)(?:,(\w+))?\)', item)
    match = re.match(r'(\w+)\(([^,]+)(?:,(.+))?\)', item)
    if match:
        class_name = match.group(1)
        args = [match.group(2)]
        if match.group(3):
            args.append(match.group(3))
        if class_name in class_map:
            cls = class_map[class_name]
            return cls(*args)
    return item

df['generated_model_lst'] = df['generated_model'].apply(lambda x: Convert_to_lst(x))
df['generated_model_lst'] = df['generated_model_lst'].apply(lambda x: [transform_item(item) for item in x])

result2 = {
    "set_size_initial": [],
    "set_size_specialized": [],
    "specialization_percentage": [],
    "model_differs": [],
    "specialized_model": [],
    "execution_time": []
}
df_result = pd.DataFrame(result2)

df_result.to_csv("specialized_model{0}.csv".format(argv[1]), sep=',',index=False)

filename='specialisation.decl'

# Run Specializer
initial_model = df.generated_model_lst.iloc[int(argv[1])]
percentage = random.random()

st = time.time()
specialized = SpecializedModel(filename,initial_model, percentage)
et = time.time()

exec_time = et - st

print(specialized.constraint_list)

fields2 = [len(initial_model),  
            len(specialized.constraint_list),
            percentage,
            specialized.model_differs,
            specialized.constraint_list,
            exec_time]

with open(r"specialized_model{0}.csv".format(argv[1]), 'a') as f:
    writer = csv.writer(f)
    writer.writerow(fields2)

# for series_name, series in df.generated_model.items():
#     initial_model = series
#     percentage = random.random()

#     st = time.time()
#     specialized = SpecializedModel(filename,initial_model, percentage)
#     et = time.time()

#     exec_time = et - st

#     print(specialized.constraint_list)

#     fields2 = [len(initial_model),  
#                len(specialized.constraint_list),
#                percentage,
#                specialized.model_differs,
#                specialized.constraint_list,
#                exec_time]

#     with open(r"specialized_model{0}.csv".format(argv[1]), 'a') as f:
#         writer = csv.writer(f)
#         writer.writerow(fields2)