from Classes.Constraint import *
from Classes.Templates import *
from Classes.Alphabet import *
from Classes.ConstraintList import *
from Classes.LtlList import *
from Classes.ConstraintFactory import *
from Classes.Hierarchy import *
from Classes.Model import *
import random
from black_sat import *

class GeneralizedModel: 
    constraint = Constraint()
    constraintlist = ConstraintList()
    sigma = alphabet() # needed for satisfyability and redundancy checks with black_sat

    inconsistent_constraint = 0
    redundant_constraint = 0
    time_exceeded = 0
    model_differs = 0

    def __init__(self, filename, initial_model, generalisation_percentage = 1, deletion_percentage = 0, subset_to_keep = []):
        self.constraint_list = self.generalise_model(initial_model, generalisation_percentage, deletion_percentage, subset_to_keep)
        
        self.ltl_list = self.model_to_ltl(self.constraint_list)
        self.ltl_list_str = self.model_to_ltl_str()
        self.file = self.save_model(self.constraint_list, filename) 

    def generalise_model(self, initial_model, generalisation_percentage, deletion_percentage, subset_to_keep): # user can indicate to keep a part of the initial model in the generalized model
        # to empty list if you already generalized once 
        constraint = Constraint()
        ltl_list = LtlList()

        # Transform list to constraintlist 
        initial_model = ConstraintList(initial_model)
        # initial_model.__dict__ = constraint_lst_temp.__dict__

        # Transform to LTL list
        generalized_model = self.model_to_ltl(subset_to_keep) 

        # if subset_to_keep == []:
        #     generalized_model = []
        # else: generalized_model = generalized_model

        self.inconsistent_constraint = 0
        self.redundant_constraint = 0
        self.time_exceeded = 0 
        self.model_differs = 0 # salver took longer than 1 minute 

        stop_after = 10

        n = 0 # number of times that a constraint was consequently not added to the model
        self.iterations = [] # to save how many iterations were needed before adding a constraint to the model 

        hierarchy = Hierarchy()
        n_initial_model = len(initial_model)

        if n_initial_model == 0: 
            return Model.cf.end_model_message("No generalisation of initial model could be generated, because initial model is empty.")
        else:
            for index in range(0, n_initial_model):
                initial_constraint = initial_model[index]
                # generalized model to LTL list
                generalized_model_ltl = self.model_to_ltl(generalized_model)

                if hierarchy.can_be_generalised(initial_constraint): 
                    if random.random() < generalisation_percentage:
                        # Generalisation: by hierarchy or by deleting constraint from initial model - 50 percent chance
                        if random.random() < deletion_percentage:
                            self.iterations.append(n+1)
                            continue
                        else:    
                            potential_constraint = hierarchy.generate_generalisation_candidate(initial_constraint)
                            ltl_constraint = self.constraint.declare_to_ltl(potential_constraint, self.sigma)
                            consistency = ltl_list.check_consistency(ltl_constraint, generalized_model_ltl, self.sigma, time_out=30)
                            redundancy = ltl_list.check_redundancy(ltl_constraint, generalized_model_ltl, self.sigma, time_out=30) 

                            if (consistency == True and redundancy == True):
                                generalized_model.append(potential_constraint)
                                ltl_list.append(ltl_constraint)
                                print("constraint added to generalized model")

                                self.iterations.append(n+1)
                                n = 0

                            elif (consistency == False and redundancy == False):
                                n += 1
                                self.inconsistent_constraint +=1
                                self.redundant_constraint +=1
                                print("constraint not added to model")
                                if n >= stop_after: 
                                    self.end_model_message("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
                                    # self.get_inconsistency()
                                    # self.get_redundancy()  
                                    # print(constraint_list) 
                                    self.iterations.append(n+1)
                                    self.model_differs = 1                         
                                    return generalized_model
                                else: continue 

                            elif (consistency == True and redundancy == False):
                                n += 1
                                self.redundant_constraint +=1
                                print("constraint not added to model")
                                if n >= stop_after:  
                                    self.end_model_message("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
                                    # self.get_inconsistency()
                                    # self.get_redundancy()
                                    # print(constraint_list)
                                    self.iterations.append(n+1)
                                    self.model_differs = 1
                                    return generalized_model
                                else: continue 

                            elif (consistency == False and redundancy == True):
                                n += 1
                                self.inconsistent_constraint +=1
                                print("constraint not added to model")
                                if n >= stop_after:  
                                    self.end_model_message("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
                                    # self.get_inconsistency()
                                    # self.get_redundancy()
                                    # print(constraint_list)
                                    self.iterations.append(n+1)
                                    self.model_differs = 1
                                    return generalized_model
                                else: continue 

                            elif (consistency == None or redundancy == None):
                                n += 1
                                self.time_exceeded += 1
                                print("constraint not added to model")
                                if n >= stop_after:  
                                    self.end_model_message("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
                                    # self.get_inconsistency()
                                    # self.get_redundancy()
                                    # print(constraint_list)
                                    self.iterations.append(n+1)
                                    self.model_differs = 1
                                    return generalized_model
                                else: continue
                                
                                # return constraint_list 

                            else: 
                                n += 1 
                                if n >= stop_after: 
                                    self.end_model_message("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
                                    # self.get_inconsistency()
                                    # self.get_redundancy()     
                                    # print(constraint)   
                                    self.model_differs = 1   
                                    self.iterations.append(n+1)                
                                    return generalized_model
                                else: continue
                       
                        # if not self.initial_model.contains_constraint(potential_constraint, generalized_model): 
                        #     generalized_model.append(potential_constraint)
                        # else: pass
                    
                    else:
                        potential_constraint = initial_constraint
                        ltl_constraint = self.constraint.declare_to_ltl(potential_constraint, self.sigma)
                        consistency = ltl_list.check_consistency(ltl_constraint, generalized_model_ltl, self.sigma, time_out=30)
                        redundancy = ltl_list.check_redundancy(ltl_constraint, generalized_model_ltl, self.sigma, time_out=30) 
                        if (consistency == True and redundancy == True):
                            generalized_model.append(potential_constraint)
                            ltl_list.append(ltl_constraint)
                            print("constraint added to generalized model")

                            self.iterations.append(n+1)
                            n = 0

                        elif (consistency == False and redundancy == False):
                            n += 1
                            self.inconsistent_constraint +=1
                            self.redundant_constraint +=1
                            print("constraint not added to model")
                            if n >= stop_after: 
                                self.end_model_message("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
                                # self.get_inconsistency()
                                # self.get_redundancy()  
                                # print(constraint_list) 
                                self.iterations.append(n+1)
                                self.model_differs = 1                         
                                return generalized_model
                            else: continue 

                        elif (consistency == True and redundancy == False):
                            n += 1
                            self.redundant_constraint +=1
                            print("constraint not added to model")
                            if n >= stop_after:  
                                self.end_model_message("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
                                # self.get_inconsistency()
                                # self.get_redundancy()
                                # print(constraint_list)
                                self.iterations.append(n+1)
                                self.model_differs = 1
                                return generalized_model
                            else: continue 

                        elif (consistency == False and redundancy == True):
                            n += 1
                            self.inconsistent_constraint +=1
                            print("constraint not added to model")
                            if n >= stop_after:  
                                self.end_model_message("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
                                # self.get_inconsistency()
                                # self.get_redundancy()
                                # print(constraint_list)
                                self.iterations.append(n+1)
                                self.model_differs = 1
                                return generalized_model
                            else: continue 

                        elif (consistency == None or redundancy == None):
                            n += 1
                            self.time_exceeded += 1
                            print("constraint not added to model")
                            if n >= stop_after:  
                                self.end_model_message("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
                                # self.get_inconsistency()
                                # self.get_redundancy()
                                # print(constraint_list)
                                self.iterations.append(n+1)
                                self.model_differs = 1
                                return generalized_model
                            else: continue
                            
                            # return constraint_list 

                        else: 
                            n += 1 
                            if n >= stop_after: 
                                self.end_model_message("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
                                # self.get_inconsistency()
                                # self.get_redundancy()     
                                # print(constraint)   
                                self.model_differs = 1   
                                self.iterations.append(n+1)                
                                return generalized_model
                            else: continue

                else: # cannot be generalized 
                    if random.random() < deletion_percentage:
                        self.iterations.append(n+1)
                        continue
                    else:
                        if not initial_model.contains_constraint(initial_constraint, generalized_model): 
                            potential_constraint = initial_constraint
                            ltl_constraint = self.constraint.declare_to_ltl(potential_constraint, self.sigma)
                            consistency = ltl_list.check_consistency(ltl_constraint, generalized_model_ltl, self.sigma, time_out=30)
                            redundancy = ltl_list.check_redundancy(ltl_constraint, generalized_model_ltl, self.sigma, time_out=30) 
                            if (consistency == True and redundancy == True):
                                generalized_model.append(potential_constraint)
                                ltl_list.append(ltl_constraint)
                                print("constraint added to generalized model")

                                self.iterations.append(n+1)
                                n = 0

                            elif (consistency == False and redundancy == False):
                                n += 1
                                self.inconsistent_constraint +=1
                                self.redundant_constraint +=1
                                print("constraint not added to model")
                                if n >= stop_after: 
                                    self.end_model_message("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
                                    # self.get_inconsistency()
                                    # self.get_redundancy()  
                                    # print(constraint_list) 
                                    self.iterations.append(n+1)
                                    self.model_differs = 1                         
                                    return generalized_model
                                else: continue 

                            elif (consistency == True and redundancy == False):
                                n += 1
                                self.redundant_constraint +=1
                                print("constraint not added to model")
                                if n >= stop_after:  
                                    self.end_model_message("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
                                    # self.get_inconsistency()
                                    # self.get_redundancy()
                                    # print(constraint_list)
                                    self.iterations.append(n+1)
                                    self.model_differs = 1
                                    return generalized_model
                                else: continue 

                            elif (consistency == False and redundancy == True):
                                n += 1
                                self.inconsistent_constraint +=1
                                print("constraint not added to model")
                                if n >= stop_after:  
                                    self.end_model_message("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
                                    # self.get_inconsistency()
                                    # self.get_redundancy()
                                    # print(constraint_list)
                                    self.iterations.append(n+1)
                                    self.model_differs = 1
                                    return generalized_model
                                else: continue 

                            elif (consistency == None or redundancy == None):
                                n += 1
                                self.time_exceeded += 1
                                print("constraint not added to model")
                                if n >= stop_after:  
                                    self.end_model_message("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
                                    # self.get_inconsistency()
                                    # self.get_redundancy()
                                    # print(constraint_list)
                                    self.iterations.append(n+1)
                                    self.model_differs = 1
                                    return generalized_model
                                else: continue
                                
                                # return constraint_list 

                            else: 
                                n += 1 
                                if n >= stop_after: 
                                    self.end_model_message("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
                                    # self.get_inconsistency()
                                    # self.get_redundancy()     
                                    # print(constraint)   
                                    self.model_differs = 1   
                                    self.iterations.append(n+1)                
                                    return generalized_model
                                else: continue      

        return generalized_model

    def has_generalisation_in_model(self, constraint, generalized_model): # In generalized model
        generalized_model_class = [generalized_constraint.__class__ for generalized_constraint in generalized_model]
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

            candidate_list = Hierarchy.generalisation_candidates[constraint.__class__.__name__]

            potential_templates = list(set(candidate_list) & set(generalized_model_class))

            if potential_templates == []: 
                return False 
            else: 
                potential_constraints = []
                for i in range(len(potential_templates)): 
                    for j in range(len(generalized_model)):
                        if potential_templates[i] == generalized_model_class[j]:
                            potential_constraints.append(generalized_model[j])

                potential_constraints_str = [str(i) for i in potential_constraints]

                action = constraint.get_action()
                reaction = constraint.get_reaction()

                return any("{0},{1}".format(action,reaction) in i for i in potential_constraints_str)

        elif constraint.__class__.__name__ == 'Absence' or constraint.__class__.__name__ == 'Existence':
            return True 

        else: 
            return False 
    
    def model_to_ltl(self, constraint_list):
        constraint = Constraint()
        ltl_list = []
        if constraint_list != None:
            for i in constraint_list:
                ltl_expression = constraint.declare_to_ltl(i, self.sigma)
                ltl_list.append(ltl_expression)
        return ltl_list
    
    def model_to_ltl_str(self):
        constraint = Constraint()
        ltl_list_str = []
        if self.constraint_list != None:
            for i in self.constraint_list:
                ltl_expression = constraint.declare_to_ltl(i, self.sigma)
                ltl_list_str.append(str(ltl_expression))
        return ltl_list_str
    
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

    def save_model(self, constraint_list, filename):
        file = open(filename, 'w',  encoding="utf-8") # overwrite if file already exists
        output = Model.constraintlist.list_to_decl_extension(constraint_list, activities=[])
        file.write(str(output))
        file.close()

    




