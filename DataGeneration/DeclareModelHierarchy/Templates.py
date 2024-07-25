from Classes.Constraint import *
from Classes.Alphabet  import *

class Templates:
    
    # def __init__(self, templates):
    #     if templates == []: 
    #         self.templates = [Init, 
    #                       End, 
    #                       CoExistence, 
    #                       RespondedExistence, 
    #                       Response, 
    #                       Precedence, 
    #                       Succession, 
    #                       AlternateResponse, 
    #                       AlternatePrecedence, 
    #                       AlternateSuccession, 
    #                       ChainResponse, 
    #                       ChainPrecedence, 
    #                       ChainSuccession,
    #                       NotCoExistence, 
    #                       NotSuccession, 
    #                       NotChainSuccession,
    #                       Absence, 
    #                       Exactly,
    #                       Existence,
    #                       Choice,
    #                       ExclusiveChoice]
    #     else: self.templates = templates

    def __init__(self, templates):
        if templates == []: 
            self.templates = [Init, 
                          End, 
                          #CoExistence, 
                          RespondedExistence, 
                          Response, 
                          Precedence, 
                          #Succession, 
                          AlternateResponse, 
                          AlternatePrecedence, 
                          #AlternateSuccession, 
                          ChainResponse, 
                          ChainPrecedence]
                          #ChainSuccession,
                          #NotCoExistence] 
                          #NotSuccession, 
                          #NotChainSuccession,
                          #Absence, 
                          #Exactly,
                          #Existence]
                          #Choice,
                          #ExclusiveChoice]
        else: self.templates = templates

        # if templates == []: 
        #     self.templates = [Init, 
        #                   End, 
        #                   #CoExistence, 
        #                   RespondedExistence, 
        #                   Response, 
        #                   Precedence, 
        #                   #Succession, 
        #                   AlternateResponse, 
        #                   AlternatePrecedence, 
        #                   #AlternateSuccession, 
        #                   ChainResponse, 
        #                   ChainPrecedence,
        #                   ChainSuccession]
        #                   #NotCoExistence] 
        #                   #NotSuccession, 
        #                   #NotChainSuccession,
        #                   #Absence, 
        #                   #Exactly,
        #                   #Existence]
        #                   #Choice,
        #                   #ExclusiveChoice]
        # else: self.templates = templates

    def change_templates(self, constraint, alphabet): # Delete templates drom template_list if there are no templates left: end message 
        if constraint.__class__.has_reaction():
            # check both the ante alpha and conse alpha
            constraint_actions = alphabet.alphabet_ante.get(constraint.__class__)
            constraint_reactions = alphabet.alphabet_conse.get(constraint.__class__)
            if ((len(constraint_actions) == 0) or (len(constraint_reactions) == 0)):
                # delete constraint template from templates
                self.templates.remove(constraint.__class__)
                return constraint.__class__
            else: return None 
        else: 
            if constraint.__class__.__name__ == 'Init' or constraint.__class__.__name__ == "End":
                self.templates.remove(constraint.__class__)
                return constraint.__class__
            else:
                constraint_actions = alphabet.alphabet_ante.get(constraint.__class__)
                if (len(constraint_actions) == 0):
                    self.templates.remove(constraint.__class__)
                    return constraint.__class__
                else: return None   

    def delete_template_weight(self, deleted_template, initial_templates, weights):
        template_index = initial_templates.index(deleted_template)
        del weights[template_index]
        del initial_templates[template_index]
