# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 15:56:11 2019

@author: Dylan
"""

# -*- coding: utf-8 -*-

import numpy as np
import cvxpy as cvx
#---------------------- problem 5 --------------------------#
A1 = np.array([[2,6,-2,10],
               [-6, -4, -3, -6],
               [0,4,-3,-8]]);
A2 = np.array([[0, 1, 2, 3],
               [1, 0, 1, 2],
               [0, 1, 0, 1],
               [-1, 0, 1 ,0]]);
Arr = [A1,A2];
ind = 1;
for A in Arr:
    print "for array: " , ind;
    n, m = A.shape;
    x = cvx.Variable(n);
    p = cvx.Variable(1);
    ones = np.ones(m);
    
    obj = cvx.Minimize(p);
    constraints = [x >= 0, sum(x) == 1, A.T*(x) <= p*ones];
    
    security = cvx.Problem(obj, constraints);
    optSecurity = security.solve();
    
    y = cvx.Variable(m);
    q = cvx.Variable(1);
    ones = np.ones(n);
    
    objy = cvx.Maximize(q);
    constraintsy = [y >= 0, sum(y) == 1, A*y >= q*ones];
    
    ySecurity = cvx.Problem(objy, constraintsy);
    optySecurity = ySecurity.solve();

    print "security level: ", p.value, "  ", q.value;
    print "security policy x: ", x.value;
    print "security policy y: ", y.value;
    ind += 1;


#---------------------- problem 6 --------------------------#
A = np.array([[1,-1],
              [-1, 1]]);
print "-------------- matching pennies ----------------";
n, m = A.shape;
x = cvx.Variable(n);
p = cvx.Variable(1);
ones = np.ones(m);

obj = cvx.Maximize(p);
constraints = [x >= 0, sum(x) == 1, A.T*(x) >= p*ones];

security = cvx.Problem(obj, constraints);
optSecurity = security.solve();

y = cvx.Variable(m);
q = cvx.Variable(1);
ones = np.ones(n);

objy = cvx.Maximize(q);
constraintsy = [y >= 0, sum(y) == 1, A*y >= q*ones];

ySecurity = cvx.Problem(objy, constraintsy);
optySecurity = ySecurity.solve();

print "security level: ", p.value, "  ", q.value;
print "security policy even: ", x.value;
print "security policy odd: ", y.value;