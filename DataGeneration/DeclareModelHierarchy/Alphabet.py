from Classes.Constraint import *

class Alphabet:
    alphabet_ante = None
    alphabet_conse = None
    alphabet = []

    def __init__(self, alphabet_size):
        self.alphabet = []
        start = ord('a')
        for i in range(alphabet_size):
            self.alphabet.append(chr(start + i))

        keylist_ante = [Choice, ExclusiveChoice, Init, End, Absence, Existence, Exactly, CoExistence, RespondedExistence, Response, Precedence, Succession, AlternateResponse, \
            AlternatePrecedence, AlternateSuccession, ChainResponse, ChainPrecedence, ChainSuccession, NotCoExistence, NotSuccession, NotChainSuccession]

        keylist_conse = [Choice, ExclusiveChoice, CoExistence, RespondedExistence, Response, Precedence, Succession, AlternateResponse, AlternatePrecedence, \
            AlternateSuccession, ChainResponse, ChainPrecedence, ChainSuccession, NotCoExistence, NotSuccession, NotChainSuccession]

        self.alphabet_ante = {key: self.alphabet[:] for key in keylist_ante} 
        self.alphabet_conse = {key: self.alphabet[:] for key in keylist_conse}
  
    def change_alphabet_A(self, constraint, alphabet_A = alphabet_ante):
        if constraint.__class__.__name__ == 'Existence':
            # templates that can only occur once with the same action -- delete action
            action = constraint.get_action()
            alphabet_A[Existence].remove(str(action))
            return alphabet_A
        elif constraint.__class__.__name__ == 'Exactly':
            action = constraint.get_action()
            alphabet_A[Exactly].remove(str(action))
            return alphabet_A
        elif constraint.__class__.__name__ == 'AlternateResponse':
            action = constraint.get_action()
            alphabet_A[AlternateResponse].remove(str(action)) 
            return alphabet_A
        elif constraint.__class__.__name__ == 'AlternatePrecedence':
            action = constraint.get_action()
            alphabet_A[AlternatePrecedence].remove(str(action))
            return alphabet_A
        elif constraint.__class__.__name__ == 'AlternateSuccession':
            action = constraint.get_action()
            alphabet_A[AlternateSuccession].remove(str(action))
            return alphabet_A
        elif constraint.__class__.__name__ == 'ChainResponse':
            action = constraint.get_action()
            alphabet_A[ChainResponse].remove(str(action))
            return alphabet_A.get(ChainResponse)
        elif constraint.__class__.__name__ == 'ChainPrecedence':
            action = constraint.get_action()
            alphabet_A[ChainPrecedence].remove(str(action))
            return alphabet_A
        elif constraint.__class__.__name__ == 'ChainSuccession': 
            action = constraint.get_action()
            alphabet_A[ChainSuccession].remove(str(action))
            return alphabet_A
        # templates that cannot occur together with the same action and reaction
        elif constraint.__class__.__name__ == 'CoExistence':
            # delete action and reaction
            action = constraint.get_action()
            alphabet_A[CoExistence].remove(str(action))
            return alphabet_A
        elif constraint.__class__.__name__ == 'NotCoExistence':
            action = constraint.get_action()
            alphabet_A[NotCoExistence].remove(str(action))
            return alphabet_A
        elif constraint.__class__.__name__ == 'Succession':
            action = constraint.get_action()
            alphabet_A[Succession].remove(str(action))
            return alphabet_A  
        elif constraint.__class__.__name__ == 'NotSuccession':
            action = constraint.get_action()
            alphabet_A[NotSuccession].remove(str(action))
            return alphabet_A
        elif constraint.__class__.__name__ == 'NotChainSuccession':
            action = constraint.get_action()
            alphabet_A[NotChainSuccession].remove(str(action))
            return alphabet_A                  
        else:
            return alphabet_A

    def change_alphabet_C(self, constraint, alphabet_C = alphabet_conse):
        if constraint.__class__.__name__ == 'CoExistence':
            # templates that cannot occur together with the same action and reaction
            # delete action and reaction
            reaction = constraint.get_reaction()
            alphabet_C[CoExistence].remove(str(reaction))
            return alphabet_C
        elif constraint.__class__.__name__ == 'NotCoExistence':
            reaction = constraint.get_reaction()
            alphabet_C[NotCoExistence].remove(str(reaction))
            return alphabet_C
        elif constraint.__class__.__name__ == 'Succession':
            reaction = constraint.get_reaction()
            alphabet_C[Succession].remove(str(reaction))
            return alphabet_C 
        elif constraint.__class__.__name__ == 'NotSuccession':
            reaction = constraint.get_reaction()
            alphabet_C[NotSuccession].remove(str(reaction))
            return alphabet_C
        elif constraint.__class__.__name__ == 'NotChainSuccession':
            reaction = constraint.get_reaction()
            alphabet_C[NotChainSuccession].remove(str(reaction))
            return alphabet_C             
        else: 
            return alphabet_C