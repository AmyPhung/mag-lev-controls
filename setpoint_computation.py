"""
Compute setpoint that makes constants go to zero
"""

import sympy
from math import pi
import json

# Load in constants from json file
f = open('constants.json')
c = json.load(f)

Y_bar = sympy.symbols('Y_bar')

# Constants
I_bar = (c['m']*c['g'] * c['L']*2*pi * Y_bar**2) / \
        (c['mu']*c['N']*c['A']*c['m2'])

sympy.plot(I_bar, (Y_bar,0,0.1),
    xlabel='Y_bar (position setpoint) [m]',
    ylabel='I_bar (current setpoint) [A]')
