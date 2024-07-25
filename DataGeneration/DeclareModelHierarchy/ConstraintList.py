from Classes.Constraint import *
import re


class ConstraintList(list):
    """This class creates a list of constraints"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def check_if_exists(self, x, ls):
        if x in ls:
            return True
        else:
            return False 

    # Check for obvious inconsistencies
    def contains_constraint(self, constraint, constraint_list):
        if constraint == None: 
            return True
        else:
            constraint_list_str = [str(x) for x in constraint_list]
            if constraint.__class__.__name__ == 'Init':
                # templates that can only occur once in the model    
                startswith_ls = [x.startswith('Init') for x in constraint_list_str]
                return ConstraintList.check_if_exists(self, True, startswith_ls)
            elif constraint.__class__.__name__ == 'End':
                startswith_ls = [x.startswith('End') for x in constraint_list_str]
                return ConstraintList.check_if_exists(self, True, startswith_ls)               
            else: 
                return False

    def list_to_decl_extension(self, constraint_list, activities):
        output_activities = ""
        output_constraints = ""

        if constraint_list != [] and constraint_list != None:
            for item in activities:
                item_str = "activity " + str(item) + "\n"
                output_activities += item_str

            output1 = ""
            output2 = ""

            for item in constraint_list[:-1]:
                item_str = str(item) + " | | |\n"
                item_str = item_str.replace("(","[")
                item_str = item_str.replace(")","]")
                item_str = item_str.replace(",",", ")
                item_split = re.findall('[A-Z][^A-Z]*', item_str)
                item_str = " ".join(str(item) for item in item_split)
                output1 += item_str

            # last item constraint_list
            item_last_str = str(constraint_list[len(constraint_list)-1]) + " | | |"
            item_last_str = item_last_str.replace("(","[")
            item_last_str = item_last_str.replace(")","]")
            item_last_str = item_last_str.replace(",",", ")
            item_split = re.findall('[A-Z][^A-Z]*', item_last_str)
            item_last_str = " ".join(str(item) for item in item_split)
            output2 = item_last_str

            output_constraints = output1 + output2

            output = output_activities + output_constraints

            return output
        else: return ""