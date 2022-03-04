from collections import deque
import numpy as np
from tokens import Token, TokenType

def tokenize(s):
    '''Converts a string into a list of tokens
    
    args: 
        s (string)
    return: 
        tkns (list)
    '''
    tkn = ''
    tkns = []
    # Create an empty token in order to use the check_type func
    empty_token = Token(None)
    char_type = empty_token.check_type(s[0])
    
    # Separates tokens by checking for changes in their type
    for char in s:
        if char == ' ':
            continue
        
        new_type = empty_token.check_type(char)
        if new_type != char_type:
            tkns.append(Token(tkn))
            tkn = char
            char_type = new_type
        else:
            tkn += char
            
    tkns.append(Token(tkn))
    
    return tkns

def peek(stack):
    '''Peeks the value from the top of the stack
    
    args:
        stack (stack)
    returns:
        value (any)
    '''
    val = stack.pop()
    stack.append(val)
    return val

def convert_equation(tokens):
    '''Converts the tokens of an equation into Reverse Polish Notation
    
    args: 
        tokens (list)
    returns: 
        output (list)
    '''
    stack = deque()
    output = []
    
    # Algorithm from https://www.chris-j.co.uk/parsing.php
    for tkn in tokens:
        if tkn.type == TokenType.NUM:
            output.append(tkn)
        elif tkn.type == TokenType.FUNC:
            stack.append(tkn)
        elif tkn.type == TokenType.LPAR:
            stack.append(tkn)
        elif tkn.type == TokenType.RPAR:
            while stack:
                op = stack.pop()
                if op.type == TokenType.LPAR:
                    break
                output.append(op)
            if peek(stack).type == TokenType.FUNC:
                output.append(stack.pop()) 
        elif tkn.type == TokenType.OP:
            if not stack or peek(stack).type == TokenType.LPAR:
                stack.append(tkn)
            else:
                repeat = True
                while stack:
                    dif = tkn.precedence - peek(stack).precedence
                    if dif > 0 or (dif == 0 and tkn.assoc == 1):
                        stack.append(tkn)
                        repeat = False
                        break
                    elif dif < 0 or (dif == 0 and tkn.assoc == 0):
                        output.append(stack.pop())
                if repeat:
                    stack.append(tkn)
    while stack:
        output.append(stack.pop())
            
    return output

def eval_func(func, val):
    '''Converts a string into its respective function and
    returns the evaluation of the function and value.
    
    args:
        func (string) function
        val (float) value
    returns:
        output (float)
    '''
    funcs = {'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
             'arcsin': np.arcsin, 'arccos': np.arccos, 'arctan': np.arctan,
             'sinh': np.sinh, 'cosh': np.cosh, 'tanh': np.tanh,
             'arcsinh': np.arcsinh, 'arccosh': np.arccosh, 'arctanh': np.arctanh,
             'ln': np.log, 'log': np.log,
             'sqrt': np.sqrt, 'abs': np.abs}
    f = funcs[func]
    return f(val)

def evaluate(eqn):
    '''Evaluates an RPN equation
    
    args:
        eqn (list) Equation in Reverse Polish Notation 
    returns:
        value (float)
    '''
    stack = deque()
    for tkn in eqn:
        if tkn.type == TokenType.NUM:
            stack.append(tkn)
        elif tkn.type == TokenType.OP:
            o1 = str(stack.pop().value)
            o2 = str(stack.pop().value)
            operator = tkn.string if tkn.string != '^' else '**'
            stack.append(Token(eval(o2 + operator + o1)))
        elif tkn.type == TokenType.FUNC:
            o1 = stack.pop().value
            # Look up the tkn in a dict and eval using associated library
            stack.append(Token(eval_func(tkn.string, o1)))
    return float(stack.pop().string)

if __name__ == '__main__':
    eqn = '3*sinh(x)cosh(x)ln(x) + 5(2) - e^x + sin(x)'
    #v = clean_equation(eqn)
    t = tokenize(eqn)
    #print(clean_equation(eqn))
    for a in t:
        print(a.string + ' ', end='')
    '''
    for a in t:
        print(a.string +' ', end='')
    rpn = convert_equation(t)
    print(evaluate(rpn))
    '''