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
        elif new_type in [TokenType.OP, TokenType.LPAR, TokenType.RPAR]:
            if tkn != '':
                tkns.append(Token(tkn))
            tkn = char
            char_type = new_type
        else:
            tkn += char
            
    tkns.append(Token(tkn))
    return tkns

def add_implicit_multiplication(tokens):
    changed = []
    conditions = [TokenType.FUNC, TokenType.NUM, TokenType.LPAR, TokenType.SYMBOL]
    initial = [TokenType.RPAR, TokenType.NUM, TokenType.SYMBOL]
    for i, token in enumerate(tokens):
        if i >= len(tokens) - 1:
            changed.append(token)
            break
        
        next_token = tokens[i + 1].type
        if token.type not in initial:
            changed.append(token)
            continue
        if next_token in conditions:
            changed.append(token)
            changed.append(Token('*'))
        else:
            changed.append(token)
        
    return changed
    
def change_unary_op(tokens):
    changed = []
    for i, token in enumerate(tokens):
        if token.string in ['-', '!']:
            if i == 0:
                token.type = TokenType.UNARYOP  
            elif tokens[i - 1].string in ['(', '*', '/', '-', '+']:
                token.type = TokenType.UNARYOP
        changed.append(token)
            
    return changed
            
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
        if tkn.type == TokenType.NUM or tkn.type == TokenType.SYMBOL:
            output.append(tkn)
        elif tkn.type == TokenType.FUNC:
            stack.append(tkn)
        elif tkn.type == TokenType.LPAR:
            stack.append(tkn)
        elif tkn.type == TokenType.UNARYOP:
            if tkn.string == '-':
                stack.append(tkn)
            elif tkn.string == '!':
                output.append(tkn)
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

def find_continuity(rpn, a, b):
    linear = np.linspace(a, b, 10000)
    dx = 0.00001
    indexes = []
    for i, token in enumerate(rpn):
        if token.string == Token.Variable:
            indexes.append(i)
            
    for i, num in enumerate(linear):
        for index in indexes:
            rpn[index].value = num
        y1 = evaluate(rpn)
        for index in indexes:
            rpn[index].value = num + dx
        y2 = evaluate(rpn)
        
        dy = y2 - y1
        
        if np.abs(dy) > 0.001:
            return False
    return True

def is_func_continuous(tokens):
  '''Returns whether a function is potentially continuous or not

  args:
    tokens (list) list of token objects
  returns:
    boolean
  '''
  discont = ['tan', 'cot', 'ln', 'sqrt', 'log', 'arcsec', 'arccsc']
  idx = 1
  for i, func in enumerate(tokens):
    if func.type == TokenType.FUNC:
      if func.string in discont:
        return False
      else:
        return True
    elif func.string == "^":
      num = True
      if tokens[i-1].type == TokenType.NUM:
        num = True
      elif tokens[i-1].type in [TokenType.FUNC, TokenType.SYMBOL]:
        num = False
      # number ^ number Flag True
      # number ^ variable or function: Flag False 
      # variable or function ^ number that is < 1 not equal to 0: Flag False
      # variable or function ^ variable or function: Flag False
       # 2^3 + x^2 stop after operator
        # 2^(3 + x^(2) ) + x^2stop after finding closing bracket
      left = 0
      right = 0
      left_ind=0
      right_ind = 0
      ctr = 0
      while left != right:
        if tokens[i+ctr].type == TokenType.LPAR:
          left += 1
        elif tokens[i+ctr].type == TokenType.RPAR:
          right += 1
        if left == 1:
          left_ind = i + ctr
        if right == left:
          right_ind == i + ctr
          break

        
      if not num:
        return False
      for smt in range(left_ind, right_ind +1):
        if tokens[smt].type in [TokenType.FUNC, TokenType.SYMBOL]:
          return False
      return True
      
        
    if func.string == '/':
      # Loops through all tokens that are after the division symbol
      # If a token is a symbol or function, then it is flagged as 
      # potentially discontinuous
      while tokens[i + idx].type not in [TokenType.FUNC, TokenType.SYMBOL]:
        idx += 1
        if i + idx > len(tokens) - 1:
          return True
      return False
        
def evaluate(eqn):
    '''Evaluates an RPN equation
    
    args:
        eqn (list) Equation in Reverse Polish Notation 
    returns:
        value (float)
    '''
    stack = deque()
    for tkn in eqn:
        if tkn.type == TokenType.NUM or tkn.type == TokenType.SYMBOL:
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
        elif tkn.type == TokenType.UNARYOP:
            num = str(stack.pop().value)
            op = tkn.string
            stack.append(Token(eval(op + num)))
    return float(stack.pop().string)

if __name__ == '__main__':
<<<<<<< HEAD
    eqn = '5+-3'
=======
    eqn = '4^(0.5)'
>>>>>>> c36caa2501095ac6b1e78b7ea572aaa70b929925
    t = tokenize(eqn)
    t = change_unary_op(t)
    t = add_implicit_multiplication(t)
    rpn = convert_equation(t)
    print(evaluate(rpn))