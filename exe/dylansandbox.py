# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 12:45:56 2019

@author: Dylan
"""
# Dylan testing out python

# simulates and plots Brownian motion over the time interval [0,1]

# import math
#import numpy
#import matplotlib.pyplot as plt
#import sandbox.dylansfunctions as df
#import cvxpy
#
##a = [1, 2, 2]
##b = [1, 2.1, 2]
##print df.isleq(a,b)
#
#times = numpy.linspace(0.0, 100.0, num=1025)
#
#
#for i in range(10):
#    X = df.brownbridge(times)
#    #fig, ax = plt.subplots()
#    #ax.plot(times,W)
#    #
#    #ax.set(xlabel='t', ylabel='W_t',
#    #       title='Wiener process simulation')
#    #ax.grid(True)
#    
#    #fig.savefig("test.png")
#    #plt.axes().set_aspect('equal', 'datalim')
#    #plt.show()
#    
#    
#    plt.plot(times, X, '-', lw=1)
#    
#plt.xlabel('t')
#plt.ylabel('X_t')
#plt.title('Brownian bridge simulation')
#plt.grid(True)
#plt.axes().set_aspect('equal', 'datalim')
#plt.show()

import cvxpy as cp
import numpy as np
# Problem data.
m = 30
n = 20
np.random.seed(1)
A = np.random.randn(m, n)
b = np.random.randn(m)
# Construct the problem.
x = cp.Variable(n)
objective = cp.Minimize(cp.sum_squares(A*x - b))
constraints = [0 <= x, x <= 1]
prob = cp.Problem(objective, constraints)
# The optimal objective value is returned by `prob.solve()`.
result = prob.solve()
# The optimal value for x is stored in `x.value`.
print(x.value)
# The optimal Lagrange multiplier for a constraint is stored in
# `constraint.dual_value`.
print(constraints[0].dual_value)
