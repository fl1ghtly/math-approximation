from enum import Enum
import math

class TokenType(Enum):
    FUNC = 'FUNC'
    OP = 'OP'
    NUM = 'NUM'
    LPAR = 'LPAR'
    RPAR = 'RPAR'
    
class Token:
    def __init__(self, s) -> None:
        self.string = str(s)
        self.set_type()
        self.precedence = None
        self.assoc = None
        self.value = None
        
        if self.type == TokenType.OP:
            self.set_precedence()
            self.set_association()
        elif self.type == TokenType.NUM:
            self.set_value()
            
    def set_type(self):
        if self.is_op():
            self.type = TokenType.OP
        elif self.is_func():
            self.type = TokenType.FUNC
        elif self.is_num():
            self.type = TokenType.NUM
        elif self.string == '(':
            self.type = TokenType.LPAR
        elif self.string == ')':
            self.type = TokenType.RPAR
            
    def set_value(self):
        values = {'pi': math.pi, 'e': math.e}

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
        
    def is_op(self):
        '''Checks if a string is an operator
        
        args: 
            s (string)
        returns: 
            boolean
        '''
        operators = ['+', '-', '^', '*', '/']

        if self.string in operators:
            return True
        
        return False
    def is_func(self):
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
                'ln', 'log', 'sqrt']
        if self.string in funcs:
            return True
        
        return False
    
    def is_num(self):
        '''Checks if a string is an integer
        
        args: 
            s (string)
        returns: 
            boolean
        '''
        try:
            if self.string == 'pi' or self.string == 'e':
                return True
            float(self.string)
            return True
        except:
            return False
        
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Token):
            return False

        if self.string == __o.string:
            return True
        
        return False