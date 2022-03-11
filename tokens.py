from enum import Enum
import numpy as np

class TokenType(Enum):
    FUNC = 'FUNC'
    OP = 'OP'
    UNARYOP = 'UNARYOP'
    NUM = 'NUM'
    LPAR = 'LPAR'
    RPAR = 'RPAR'
    NONE = 'NONE'
    SYMBOL = 'SYMBOl'
    
class Token:
    Variable = 'x'
    
    def __init__(self, s) -> None:
        if s is not None:
            self.string = str(s)
            self.type = self.check_type(self.string)
            self.precedence = 0
            self.assoc = 0
            self.value = None
            
            if self.type == TokenType.OP:
                self.set_precedence()
                self.set_association()
            elif self.type == TokenType.NUM:
                self.set_value()
            
    def check_type(self, s):
        if self.is_op(s):
            return TokenType.OP
        elif self.is_func(s):
            return TokenType.FUNC
        elif self.is_num(s):
            return TokenType.NUM
        elif s == self.Variable:
            return TokenType.SYMBOL
        elif s == '(':
            return TokenType.LPAR
        elif s == ')':
            return TokenType.RPAR
        
        return TokenType.NONE
            
    def set_value(self):
        values = {'pi': np.pi, 'e': np.e, self.Variable: None}

        if self.string.isalpha():
            self.value = values[self.string]
        else:
            self.value = float(self.string)

    def set_precedence(self):
        '''Returns the difference in precedence of the first operator 
        and the second operator
        
        args:
            o1 (string) operator
            o2 (string) operator
        returns:
            difference (int) difference in the two operator's precedence
        '''
        precedence = {'^': 4, '*': 3, '/': 3, '+': 2, '-': 2}

        self.precedence = precedence[self.string]
    
    def set_association(self):
        '''Returns the operator's association. 0 is left association, 
        1 is right association
        
        args:
            o (string) operator
        returns:
            associativity (int)
        '''
        associativity = {'^': 1, '*': 0, '/': 0, '+': 0, '-': 0}
        self.assoc = associativity[self.string]
        
    def is_op(self, s):
        '''Checks if a string is an operator
        
        args: 
            s (string)
        returns: 
            boolean
        '''
        operators = ['+', '-', '^', '*', '/']

        if s in operators:
            return True
        
        return False
    
    def is_func(self, s):
        '''Checks if a string is a function
        
        args:
            s (string)
        returns:
            boolean
        '''
        funcs = ['sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan',
                'csc', 'sec', 'cot', 'arccsc', 'arcsec', 'arccot',
                'sinh', 'cosh', 'tanh', 'arcsinh', 'arccosh', 'arctanh',
                'csch', 'sech', 'coth', 'arccsch', 'arcsech', 'arccoth',
                'ln', 'log', 'sqrt', 'abs']
        if s in funcs:
            return True
        
        return False
    
    def is_num(self, s):
        '''Checks if a string is an integer
        
        args: 
            s (string)
        returns: 
            boolean
        '''
        specials = ['pi', 'e', '.']
        try:
            if s in specials:
                return True
            float(s)
            return True
        except:
            return False
        
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Token):
            return False

        if self.string == __o.string:
            return True
        
        return False