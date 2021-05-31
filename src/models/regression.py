import pandas as pd
import sympy as sp
from rolldecayestimators.substitute_dynamic_symbols import lambdify
from rolldecayestimators import symbols

def get_X_lambda(eq_X):
    return lambdify(eq_X.rhs)

def calculate_features(data:pd.DataFrame, eq_X:sp.Eq, beta:sp.Eq):
    
    X_lambda = get_X_lambda(eq_X=eq_X)
    
    X = X_lambda(phi=data['phi'], phi1d=data['phi1d'])
    X = X.reshape(X.shape[1],X.shape[-1]).T
    X = pd.DataFrame(data=X, index=data.index, columns=list(beta))
    
    return X


def get_acceleration(roll_decay_equation):
    """Swap around equation to get acceleration in left hand side

    Args:
        roll_decay_equation ([type]): [description]

    Returns:
        [type]: [description]
    """

    return sp.Eq(-symbols.phi_dot_dot,
                 -sp.solve(roll_decay_equation, symbols.phi_dot_dot)[0])

def get_coefficients(acceleration_equation):

    coefficients = []
    for part in acceleration_equation.rhs.args:   
        coeff = part.subs([(symbols.phi_dot_dot,1),
                          (symbols.phi_dot,1),
                          (symbols.phi,1),
                         ])
        coefficients.append(coeff)

    return coefficients

def get_parts(acceleration_equation):

    coefficients = get_coefficients(acceleration_equation=acceleration_equation)
    parts = acceleration_equation.rhs.subs([(c,1) for c in coefficients]).args
    return parts

def get_labels_and_features(acceleration_equation):

    parts = get_parts(acceleration_equation=acceleration_equation)

    xs = [sp.symbols(f'x_{i}') for i in range(1,len(parts)+1)]
    y_ = sp.symbols('y')
    X_ = sp.MatrixSymbol('X', 1, len(xs))
    beta_ = sp.MatrixSymbol('beta', len(xs), 1)

    subs = {part:x for part,x in zip(parts,xs)}

    acceleration_equation_x = sp.Eq(y_,
                                      acceleration_equation.rhs.subs(subs))

    eq_beta = sp.Eq(beta_,
                sp.linear_eq_to_matrix([acceleration_equation_x.rhs],xs)[0].T)
    
    X_matrix = sp.Matrix(list(subs.keys())).T
    eq_X = sp.Eq(X_, 
             X_matrix)

    eq_y = sp.Eq(y_,-symbols.phi_dot_dot)

    return acceleration_equation_x, eq_beta, eq_X, eq_y