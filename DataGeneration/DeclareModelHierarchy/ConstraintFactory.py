from Classes.Constraint import *
from Classes.Alphabet import *
from Classes.ConstraintList import *
from Classes.LtlList import *
from Classes.Templates import *
from black_sat import *
import random
import copy

class ConstraintFactory:
    """This class creates random constraints by combining a constraint template with activities"""
    sigma = alphabet()

    inconsistent_constraint = 0
    redundant_constraint = 0
    time_exceeded = 0
    model_differs = 0
    
    def __init__(self):
        pass
    
    def create_consistent_model(self, alphabet_size, set_size, weights, stop_after, templates, time_out):
        constraint = Constraint()
        constraint_list = ConstraintList()
        ltl_list = LtlList()
        alphabet = Alphabet(alphabet_size)
        t = Templates(templates)
        initial_templates = copy.deepcopy(t.templates)

        ltl_list.append(ltl_list.add_first_ltl(alphabet.alphabet,self.sigma))

        self.inconsistent_constraint = 0
        self.redundant_constraint = 0
        self.time_exceeded = 0 
        self.model_differs = 0 # salver took longer than 1 minute 

        n = 0 # number of times that a constraint was consequently not added to the model
        self.iterations = [] # to save how many iterations were needed before adding a constraint to the model 
        j = 0

        while j < set_size:
            if templates != []:

                ##### uitzetten na debug
                # if j == 0: 
                #     potential_constraint = Init('d')
                # elif j == 1:
                #     potential_constraint = Existence('a') # a must exist <a>
                # elif j==2: 
                #     potential_constraint = ChainSuccession('i','a') 
                #     # i must appear in the first position before a <i,a> AND a must appear in the next posit after i
                # else:
                #     potential_constraint = ChainResponse('i','c') # c must appear in the first position after i <i,c> --> Inconsistent with two previous

                ##### terug aanzetten
                potential_constraint = self.create_one_constraint_alphabet(t.templates, weights, alphabet)
                
                print("potential_constraint created: " + str(potential_constraint))

                if potential_constraint != None:
                    ltl_constraint = constraint.declare_to_ltl(potential_constraint, self.sigma)
                    consistency = ltl_list.check_consistency(ltl_constraint, ltl_list, self.sigma, time_out)
                    redundancy = ltl_list.check_redundancy(ltl_constraint, ltl_list, self.sigma, time_out)                                 

                    if (consistency == True and redundancy == True):
                        constraint_list.append(potential_constraint)
                        ltl_list.append(ltl_constraint)
                        print("constraint added to model)")
                        deleted_template = t.change_templates(potential_constraint, alphabet)

                        if deleted_template != None:
                            t.delete_template_weight(deleted_template,initial_templates,weights)

                        self.iterations.append(n+1)
                        n = 0
                        j += 1

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
                            return constraint_list
                        else: j += 1

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
                            return constraint_list
                        else: j += 1 

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
                            return constraint_list
                        else: j += 1 

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
                            return constraint_list
                        else: j += 1
                        
                        # return constraint_list 

                else: # if potential_constraint == None
                    n += 1 
                    if n >= stop_after: 
                        self.end_model_message("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
                        # self.get_inconsistency()
                        # self.get_redundancy()     
                        # print(constraint)   
                        self.iterations.append(n+1)                
                        return constraint_list
                    else: j += 1
            
            else: # if templates list is empty
                self.end_model_message("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.") 
                # self.get_inconsistency()
                # self.get_redundancy()   
                # print(constraint_list)
                self.iterations.append(n+1) 
                self.model_differs = 1            
                return constraint_list
            
        # self.get_inconsistency()
        # self.get_redundancy()
        # print(constraint_list)
        return constraint_list

    def create_one_constraint_alphabet(self, templates, weights, alphabet, n=1):
        template_class = random.choices(templates, weights)[0]

        alpha_A = alphabet.alphabet_ante
        alpha_C = alphabet.alphabet_conse

        if template_class.has_reaction():
            if (len(alpha_A.get(template_class)) != 0 and len(alpha_C.get(template_class)) != 0): 
                constraint = template_class(action = random.choice(alpha_A.get(template_class)), reaction = random.choice(alpha_C.get(template_class)))
                alphabet.change_alphabet_A(constraint, alpha_A)
                alphabet.change_alphabet_C(constraint, alpha_C)
                return constraint
            else:
                constraint = None ##### AANPASSEN --> In dit geval is één van de alphabets leeg 
                return None

        ####################################
        # elif template_class.has_n():
        #     constraint = template_class(action = random.choice(alpha_A.get(template_class)), n = random.randint(1,n)) # ik heb nu voor n gekozen van 1 tot 5
        #     alphabet.change_alphabet_A(constraint, alpha_A)
        #     alphabet.change_alphabet_C(constraint, alpha_C)
        #     return constraint

        else: 
            if len(alpha_A.get(template_class)) != 0:
                constraint = template_class(action = random.choice(alpha_A.get(template_class)))
                alphabet.change_alphabet_A(constraint, alpha_A)
                return constraint
            else: 
                return None   
            
    def end_model_message(self, message):
        print(message)

    def get_inconsistency(self):
        # print("inconsistent_constraints: " + str(self.inconsistent_constraint))
        return self.inconsistent_constraint

    def get_redundancy(self):
        # print("redundant_constraints: " + str(self.redundant_constraint))
        return self.redundant_constraint
    
    def get_time_exceeded(self):
        return self.time_exceeded

    def get_model_differs(self):
        return self.model_differs
    
    def get_iterations_before_adding(self):
        return self.iterations

