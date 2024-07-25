from Classes.Constraint import *
from Classes.Templates import *
from Classes.Alphabet import *
from Classes.ConstraintList import *
from Classes.LtlList import *
from Classes.ConstraintFactory import *
from Classes.Hierarchy import *
import random
from black_sat import *

class Model: 
    cf = ConstraintFactory()
    constraint = Constraint()
    constraintlist = ConstraintList()
    sigma = alphabet() # needed for satisfyability and redundancy checks with black_sat

    def __init__(self, filename, alphabet_size, set_size, weights, stop_after, time_out, templates = []):
        constraint_templates = Templates(templates).templates

        self.constraint_list = Model.cf.create_consistent_model(alphabet_size, set_size, weights, stop_after, constraint_templates, time_out)
        
        self.ltl_list = self.model_to_ltl()
        self.ltl_list_str = self.model_to_ltl_str()
        self.activities = Alphabet(alphabet_size).alphabet
        self.file = self.save_model(self.constraint_list, self.activities, filename) 

    def __len__(self): # get the number of constraints in the generated model
        return len(self.constraint_list)
    
    def model_to_ltl(self):
        constraint = Constraint()
        ltl_list = []
        for i in self.constraint_list:
            ltl_expression = constraint.declare_to_ltl(i, self.sigma)
            ltl_list.append(ltl_expression)
        return ltl_list
    
    def model_to_ltl_str(self):
        constraint = Constraint()
        ltl_list_str = []
        for i in self.constraint_list:
            ltl_expression = constraint.declare_to_ltl(i, self.sigma)
            ltl_list_str.append(str(ltl_expression))
        return ltl_list_str

    def specialise_model(self, filename, specialization_percentage,specialized_model=[]): # user can indicate to keep a part of the initial model in the specialized model
        # to empty list if you already specialized once 
        if specialized_model == []:
            specialized_model = []
        else: specialized_model = specialized_model

        hierarchy = Hierarchy()
        n_initial_model = self.__len__()

        if n_initial_model == 0: 
            return Model.cf.end_model_message("No specialization of initial model could be generated, because initial model is empty.")
        else:
            for index in range(0, n_initial_model):
                initial_constraint = self.constraint_list[index]

                if hierarchy.can_be_specialised(initial_constraint): 
                    if random.random() < specialization_percentage:
                        specialized_constraint = hierarchy.generate_specialisation_candidate(initial_constraint)
                        if not self.constraint_list.contains_constraint(specialized_constraint, specialized_model): 
                            specialized_model.append(specialized_constraint)
                        else: pass
                    else:
                        specialized_model.append(initial_constraint)

                else: # cannot be specialized 
                    if not self.constraint_list.contains_constraint(initial_constraint, specialized_model): 
                        specialized_model.append(initial_constraint)       
                    else: pass         

            self.file = self.save_model(self.constraint_list, self.activities, filename) 

            return specialized_model

    def has_specialisation_in_model(self, constraint, specialized_model): # In specialized model
        specialized_model_class = [specialized_constraint.__class__ for specialized_constraint in specialized_model]
        if constraint.__class__.__name__ == 'Precedence' or \
           constraint.__class__.__name__ == 'Response' or \
           constraint.__class__.__name__ == 'Succession' or \
           constraint.__class__.__name__ == 'AlternatePrecedence' or \
           constraint.__class__.__name__ == 'AlternateResponse' or \
           constraint.__class__.__name__ == 'AlternateSuccession' or \
           constraint.__class__.__name__ == 'ChainPrecedence' or \
           constraint.__class__.__name__ == 'ChainResponse' or \
           constraint.__class__.__name__ == 'RespondedExistence' or \
           constraint.__class__.__name__ == 'CoExistence' or \
           constraint.__class__.__name__ == 'NotSuccession' or \
           constraint.__class__.__name__ == 'NotChainSuccession' or \
           constraint.__class__.__name__ == 'Choice':

            candidate_list = Hierarchy.specialisation_candidates[constraint.__class__.__name__]

            potential_templates = list(set(candidate_list) & set(specialized_model_class))

            if potential_templates == []: 
                return False 
            else: 
                potential_constraints = []
                for i in range(len(potential_templates)): 
                    for j in range(len(specialized_model)):
                        if potential_templates[i] == specialized_model_class[j]:
                            potential_constraints.append(specialized_model[j])

                potential_constraints_str = [str(i) for i in potential_constraints]

                action = constraint.get_action()
                reaction = constraint.get_reaction()

                return any("{0},{1}".format(action,reaction) in i for i in potential_constraints_str)

        elif constraint.__class__.__name__ == 'Absence' or constraint.__class__.__name__ == 'Existence':
            return True 

        else: 
            return False 
    
    def get_inconsistency(self):
        return Model.cf.get_inconsistency()

    def get_redundancy(self):
        return Model.cf.get_redundancy()
    
    def get_time_exceeded(self):
        return Model.cf.get_time_exceeded()
    
    def get_model_differs(self):
        return Model.cf.get_model_differs()
    
    def get_iterations(self):
        return Model.cf.get_iterations_before_adding()

    def save_model(self, constraint_list, activities, filename):
        file = open(filename, 'w',  encoding="utf-8") # overwrite if file already exists
        output = Model.constraintlist.list_to_decl_extension(constraint_list, activities)
        file.write(str(output))
        file.close()