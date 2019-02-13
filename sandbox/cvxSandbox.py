# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 14:31:31 2019

@author: Dylan
"""

import numpy as np
import cvxpy as cvx

# maximize dot(c,x) s.t. Ax<=b, x>=0
A = np.array([
        [5.0, 3.0, 2.0, 2.0, 1.0],
        ])
b = np.array([
        8.0,
        ])
c = np.array([
        4.0, 7.0, 3.0, 5.0, 4.0,
        ])
m,n = A.shape
x = cvx.Variable(n, nonneg=True)
objective = cvx.Maximize(c*x)
constraints = [A*x <= b, x <= 1]
theProgram = cvx.Problem(objective, constraints)
theProgram.solve()
xstar = x.value