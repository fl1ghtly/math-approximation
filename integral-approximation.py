import numpy as np
import equationParser as ep
from tokens import Token

# TODO implement different point sampling
def integrate_monte_carlo(eqn, n, left, right):
    x = np.random.uniform(left, right, n)
    indexes = []
    for i, token in enumerate(eqn):
        if token.string == Token.Variable:
            indexes.append(i)
    
    y = np.zeros(n)
    for i, num in enumerate(x):
        for index in indexes:
            eqn[index].value = num
        y[i] = ep.evaluate(eqn) * (right - left)
            
    return np.average(y)

def main():
    equation = input('Input Equation: ')
    # TODO check for integer
    left = float(input('Input left endpoint: '))
    right = float(input('Input right endpoint: '))
    Token.Variable = 'x'
    t = ep.tokenize(equation)
    t = ep.change_unary_op(t)
    t = ep.add_implicit_multiplication(t)
    rpn = ep.convert_equation(t)
    print(integrate_monte_carlo(rpn, 10000, left, right))

if __name__ == '__main__':
    main()