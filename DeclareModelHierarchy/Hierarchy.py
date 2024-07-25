from Classes.Constraint import *
from Classes.ConstraintList import *
import random

class Hierarchy: 
    """This class defines hierarchies between Declare constraints in terms of specialisation"""

    # specialisation_candidates = {
    # 'ChainResponse': [ChainSuccession],
    # 'AlternateResponse': [AlternateSuccession, ChainSuccession, ChainResponse],
    # 'Response': [AlternateResponse, ChainResponse, Succession, AlternateSuccession, ChainSuccession],
    # 'RespondedExistence': [CoExistence, AlternateSuccession, ChainSuccession, Response, AlternateResponse, ChainResponse, Succession],
    # 'ChainPrecedence': [ChainSuccession],
    # 'AlternatePrecedence': [AlternateSuccession, ChainSuccession, ChainPrecedence],
    # 'Precedence': [Init, AlternatePrecedence, ChainPrecedence, Succession, AlternateSuccession, ChainSuccession],
    # 'AlternateSuccession': [ChainSuccession],
    # 'Succession': [AlternateSuccession, ChainSuccession],        
    # 'CoExistence': [Succession, AlternateSuccession, ChainSuccession],
    # 'Absence': [Exactly], # Absence
    # 'Existence': [Exactly], # Existence
    # 'NotSuccession': [NotCoExistence],
    # 'NotChainSuccession': [NotSuccession,NotCoExistence],
    # 'ExclusiveChoice': [Choice]
    # }

    # to be compliant with Declare4PY: no succession templates
    specialisation_candidates = {
    'Precedence': [Init, AlternatePrecedence, ChainPrecedence],
    'Response': [AlternateResponse, ChainResponse],
    # 'Succession': [AlternateSuccession, ChainSuccession],
    'AlternatePrecedence': [ChainPrecedence],
    'AlternateResponse': [ChainResponse],
    # 'AlternateSuccession': [ChainSuccession],
    # 'ChainPrecedence': [ChainSuccession],
    # 'ChainResponse': [ChainSuccession],
    'RespondedExistence': [CoExistence, Response, AlternateResponse, ChainResponse]
    #'CoExistence': [AlternateSuccession],
    # 'NotSuccession': [NotCoExistence],
    # 'NotChainSuccession': [NotSuccession,NotCoExistence],
    # 'ExclusiveChoice': [Choice],
    # 'Absence': [Exactly], # Absence
    # 'Existence': [Exactly] # Existence
    }

    # generalisation_candidates = { 
    # 'Response': [RespondedExistence],
    # 'AlternateResponse': [RespondedExistence,Response],
    # 'ChainResponse': [RespondedExistence,Response,AlternateResponse],
    # 'AlternatePrecedence': [Precedence],
    # 'ChainPrecedence': [Precedence,AlternatePrecedence],
    # 'Succession': [CoExistence, RespondedExistence,Response,Precedence],
    # 'AlternateSuccession': [CoExistence, RespondedExistence,Response,Precedence,Succession],
    # 'ChainSuccession': [CoExistence, RespondedExistence,Response,Precedence,Succession,ChainResponse,ChainPrecedence,AlternateSuccession,AlternatePrecedence,AlternateResponse],
    # 'NotSuccession': [NotChainSuccession],
    # 'NotChainSuccession': [NotChainSuccession,NotSuccession],
    # 'Init': [Precedence],
    # 'End': [Response],
    # 'Choice': [ExclusiveChoice],
    # 'Exactly': [Absence,Existence],
    # 'CoExistence': [RespondedExistence]
    # }

    generalisation_candidates = { 
    'Response': [RespondedExistence],
    'AlternateResponse': [RespondedExistence,Response],
    'ChainResponse': [RespondedExistence,Response,AlternateResponse],
    'AlternatePrecedence': [Precedence],
    'ChainPrecedence': [Precedence,AlternatePrecedence],
    # 'Succession': [CoExistence, RespondedExistence,Response,Precedence],
    # 'AlternateSuccession': [CoExistence, RespondedExistence,Response,Precedence,Succession],
    # 'ChainSuccession': [CoExistence, RespondedExistence,Response,Precedence,Succession,ChainResponse,ChainPrecedence,AlternateSuccession,AlternatePrecedence,AlternateResponse],
    # 'NotSuccession': [NotChainSuccession],
    # 'NotChainSuccession': [NotChainSuccession,NotSuccession],
    'Init': [Precedence],
    'Choice': [ExclusiveChoice],
    'Exactly': [Absence,Existence],
    'CoExistence': [RespondedExistence]
    }

    def __init__(self):
        pass

    # def generate_specialisation_candidate(self, constraint):
    #     if constraint.__class__.__name__ == 'Precedence' or \
    #        constraint.__class__.__name__ == 'Response' or \
    #        constraint.__class__.__name__ == 'Succession' or \
    #        constraint.__class__.__name__ == 'AlternatePrecedence' or \
    #        constraint.__class__.__name__ == 'AlternateResponse' or \
    #        constraint.__class__.__name__ == 'AlternateSuccession' or \
    #        constraint.__class__.__name__ == 'ChainPrecedence' or \
    #        constraint.__class__.__name__ == 'ChainResponse' or \
    #        constraint.__class__.__name__ == 'CoExistence' or \
    #        constraint.__class__.__name__ == 'NotSuccession' or \
    #        constraint.__class__.__name__ == 'NotChainSuccession' or \
    #        constraint.__class__.__name__ == 'Choice':
    #         action = constraint.get_action()
    #         reaction = constraint.get_reaction()
    #         specialized_template = random.choice(Hierarchy.specialisation_candidates[constraint.__class__.__name__])
    #         if specialized_template.has_reaction():
    #             specialized_constraint = specialized_template(action, reaction)                
    #         else: 
    #             specialized_constraint = specialized_template(action)    

    #     elif constraint.__class__.__name__ == 'RespondedExistence': # Een onderscheid gemaakt tussen de twee responded existences!!! (precedence vs. response)
    #         action = constraint.get_action()
    #         reaction = constraint.get_reaction()
    #         specialized_template = random.choice(Hierarchy.specialisation_candidates[constraint.__class__.__name__])
    #         #specialized_constraint = specialized_template(action, reaction)
    #         if specialized_template == "CoExistence" or specialized_template == "Succession" or specialized_template == "AlternateSuccession" or \
    #             specialized_template == "ChainSuccession":
    #             specialized_constraint = random.choice[specialized_template(action, reaction), specialized_template(reaction, action)]
    #         elif specialized_template == "Response" or specialized_template == "AlternateResponse" or specialized_template == "ChainResponse":
    #             specialized_constraint = specialized_template(action, reaction) 
    #         else: 
    #             specialized_constraint = specialized_template(reaction, action)

    #     elif constraint.__class__.__name__ == 'Existence':
    #         action = constraint.get_action()
    #         # n = constraint.get_n()
    #         specialized_template = random.choice(Hierarchy.specialisation_candidates[constraint.__class__.__name__])
    #         specialized_constraint = specialized_template(action)

    #     else: 
    #         specialized_constraint = False                  

    #     return specialized_constraint

    def generate_generalisation_candidate(self, constraint):
        if  constraint.__class__.__name__ == 'Succession' or \
            constraint.__class__.__name__ == 'AlternateSuccession' or \
            constraint.__class__.__name__ == 'ChainSuccession' or \
            constraint.__class__.__name__ == 'Response' or \
            constraint.__class__.__name__ == 'AlternateResponse' or \
            constraint.__class__.__name__ == 'ChainResponse' or \
            constraint.__class__.__name__ == 'ChainPrecedence' or \
            constraint.__class__.__name__ == 'AlternatePrecedence' or \
            constraint.__class__.__name__ == 'NotSuccession' or \
            constraint.__class__.__name__ == 'NotChainSuccession' or \
            constraint.__class__.__name__ == 'CoExistence':
            action = constraint.get_action()
            reaction = constraint.get_reaction()
            generalized_template = random.choice(Hierarchy.generalisation_candidates[constraint.__class__.__name__])
            generalized_constraint = generalized_template(action,reaction)  

        # elif constraint.__class__.__name__ == 'Init': 
        #     action = constraint.get_action()
        #     generalized_template = random.choice(Hierarchy.generalisation_candidates[constraint.__class__.__name__])
        #     generalized_constraint = generalized_template(action,random.choice(alphabet))

        # elif constraint.__class__.__name__ == 'End': 
        #     action = constraint.get_action()
        #     generalized_template = random.choice(Hierarchy.generalisation_candidates[constraint.__class__.__name__])
        #     generalized_constraint = generalized_template(random.choice(alphabet),action)

        else: 
            generalized_constraint = False                  

        return generalized_constraint
    
    def generate_specialisation_candidate(self, constraint):
        if constraint.__class__.__name__ == 'Precedence' or \
           constraint.__class__.__name__ == 'Response' or \
           constraint.__class__.__name__ == 'Succession' or \
           constraint.__class__.__name__ == 'AlternatePrecedence' or \
           constraint.__class__.__name__ == 'AlternateResponse' or \
           constraint.__class__.__name__ == 'AlternateSuccession' or \
           constraint.__class__.__name__ == 'ChainResponse' or \
           constraint.__class__.__name__ == 'ChainPrecedence' or \
           constraint.__class__.__name__ == 'AlternateResponse' or \
           constraint.__class__.__name__ == 'CoExistence':
            action = constraint.get_action()
            reaction = constraint.get_reaction()
            specialized_template = random.choice(Hierarchy.specialisation_candidates[constraint.__class__.__name__])
            if specialized_template.has_reaction():
                specialized_constraint = specialized_template(action, reaction)                
            else: 
                specialized_constraint = specialized_template(action)    

        elif constraint.__class__.__name__ == 'RespondedExistence': # Een onderscheid gemaakt tussen de twee responded existences!!! (precedence vs. response)
            action = constraint.get_action()
            reaction = constraint.get_reaction()
            specialized_template = random.choice(Hierarchy.specialisation_candidates[constraint.__class__.__name__])
            #specialized_constraint = specialized_template(action, reaction)
            if specialized_template == "CoExistence" or specialized_template == "Succession" or specialized_template == "AlternateSuccession" or \
                specialized_template == "ChainSuccession":
                specialized_constraint = random.choice[specialized_template(action, reaction), specialized_template(reaction, action)]
            else:
                specialized_constraint = specialized_template(action, reaction) 

        elif constraint.__class__.__name__ == 'Existence':
            action = constraint.get_action()
            # n = constraint.get_n()
            specialized_template = random.choice(Hierarchy.specialisation_candidates[constraint.__class__.__name__])
            specialized_constraint = specialized_template(action)

        else: 
            specialized_constraint = False                  

        return specialized_constraint
    
    def can_be_specialised(self, constraint):
        if self.generate_specialisation_candidate(constraint) == False:
            return False
        else: return True 

    def can_be_generalised(self, constraint):
        if self.generate_generalisation_candidate(constraint) == False:
            return False
        else: return True 

    def delete_specialization_candidate(self, constraint, specialisation): # Delete templates drom template_list if there are no templates left: end message 
        self.specialisation_candidates[constraint.__class__.__name__].remove(specialisation.__class__)