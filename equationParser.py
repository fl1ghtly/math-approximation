from collections import deque
import math
from tokens import Token, TokenType

def tokenize(s):
    '''Converts a string into a list of tokens
    
    args: 
        s (string)
    return: 
        tkns (list)
    '''
    breaks = ['\n', '(', ')', '+', '-', '^', '*', '/']
    tkn = ''
    tkns = []
    for letter in s:
        # Skips any spaces in the string
        if letter == ' ':
            continue
        
        # Appends the next token once a break is found
        if letter in breaks:
            # Stops adding empty spaces when two breaks are next to each other
            if tkn != '':
                tkns.append(Token(tkn))
            tkns.append(Token(letter))
            tkn = ''
        else:
            tkn += letter

    # Appends the very last token
    if tkn != '':
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
    funcs = {'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
             'arcsin': math.asin, 'arccos': math.acos, 'arctan': math.atan,
             'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
             'arcsinh': math.asinh, 'arccosh': math.acosh, 'arctanh': math.atanh,
             'ln': math.log, 'log': math.log,
             'sqrt': math.sqrt}
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

            stack.append(Token(eval(o2 + tkn.string + o1)))
        elif tkn.type == TokenType.FUNC:
            o1 = stack.pop().value
            # Look up the tkn in a dict and eval using associated library
            stack.append(Token(eval_func(tkn.string, o1)))
    return stack.pop()

if __name__ == '__main__':
    eqn = 'ln(e)'
    t = tokenize(eqn)
    rpn = convert_equation(t)
    print(evaluate(rpn).string)