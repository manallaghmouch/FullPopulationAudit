from Model import *
import pandas as pd
import time
import csv 
import random
from sys import argv

# Files
alphabet=random.randint(4,35)
set=random.randint(3,45)
stop_time=30 
time_file = time.time()

result1 = {
    "scenario": [],
    "len_given": [],
    "len_actual": [],
    "alphabet_size": [],
    "iterations":[],
    "stop_after": [],
    "inconsistencies": [],
    "redundancies": [],
    "model_differs": [],
    "exec_time_generator": [],
    "time_exceeded": [],
    "exec_time100": [],
    "exec_time70": [],
    "exec_time50": [],
    "exec_time30": []
}
df1 = pd.DataFrame(result1)
df1.to_csv("generator_setting1_{0}.csv".format(argv[1]), sep=',',index=False)

result2 = {
    "scenario": [],
    "set_size": [],
    "alphabet_size": [],
    "generated_model": [],
    "specialized100": [],
    "specialized70": [],
    "specialized50": [],
    "specialized30": [],
}
df2 = pd.DataFrame(result2)
df2.to_csv("specializer_setting1_{0}.csv".format(argv[1]), sep=',',index=False)

# Baseline parameters
stop_after = 10 # constraints
templates = [] # all templates
weights = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] # equal probability of occurrence 



# Main program
st_g = time.time()
model = Model("model_{0}.decl".format(argv[1]), alphabet_size=alphabet, set_size=set, weights=weights, stop_after=stop_after, time_out=stop_time, templates=templates)
### format toegevoegd 
et_g = time.time()

# specialization scenarios
st_s100 = time.time()
specialized100 = model.specialise_model(1)
et_s100 = time.time() 

st_s70 = time.time()
specialized70 = model.specialise_model(0.7)
et_s70 = time.time() 

st_s50 = time.time()
specialized50 = model.specialise_model(0.5)
et_s50 = time.time() 

st_s30 = time.time()
specialized30 = model.specialise_model(0.3)
et_s30 = time.time() 

# get the execution time
exec_time_generator = et_g - st_g
exec_time100 = et_s100 - st_s100
exec_time70 = et_s70 - st_s70
exec_time50 = et_s50 - st_s50
exec_time30 = et_s30 - st_s30

# print('Execution time generator:', exec_time_generator, 'seconds')
# print('Execution time specializer:', exec_time_specializer, 'seconds')

fields1 = [str(str(set) + "--" + str(alphabet)), 
            set, 
            model.__len__(), 
            alphabet, 
            stop_after, 
            model.get_iterations(),
            model.get_inconsistency(), 
            model.get_redundancy(), 
            model.get_model_differs(),
            exec_time_generator,
            model.get_time_exceeded(),
            exec_time100,
            exec_time70,
            exec_time50,
            exec_time30
            ]

with open(r"generator_setting1_{0}.csv".format(argv[1]), 'a') as f:
    writer = csv.writer(f)
    writer.writerow(fields1)

fields2 = [str(str(set) + "--" + str(alphabet)), 
            set, 
            alphabet, 
            model.constraint_list,
            specialized100,
            specialized70,
            specialized50,
            specialized30]

with open(r"specializer_setting1_{0}.csv".format(argv[1]), 'a') as f:
    writer = csv.writer(f)
    writer.writerow(fields2)
