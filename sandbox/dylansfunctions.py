# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 15:36:28 2019

@author: Dylan
"""
import numpy as np

#checks if lists a and b satisfy the elementwise inequality a <= b
def isleq(a,b):
    n = len(a)
    if len(b)==n:
        truth = True
        for i in range(n):
            if not (a[i] <= b[i]):
                truth = False
                break
        return truth
    else:
        return False


def brownbridge(times):
    # returns the Brownian bridge that is zero at the extreme values of "times"
    t0 = min(times)
    tspan = max(times) - t0
    N = len(times)
    if all(times[i] <= times[i+1] for i in range(N-1)):
        # the times are sorted
        X = wiener(times)
        Wend = X[-1]
        for i in range(N):
            X[i] = X[i] - Wend*(times[i]-t0)/tspan
        return X
    else:
        raise NotImplementedError('the function cannot work with unsorted times yet')
            

# simulates a Wiener process on an ordered list of times
def wiener(times):
    N = len(times)
    if N==0:
        return []
    elif N==1:
        return [0.0]
    elif all(times[i] <= times[i+1] for i in range(N-1)):
        # the times are sorted
        W = [0.0]
        k = 0
        while k<N-1:
            rootdt = (times[k + 1] - times[k])**0.5
            dW = np.random.randn(1)*rootdt
            W.append(W[k]+dW)
            k += 1
        return W
    else:
        raise NotImplementedError('the function cannot work with unsorted times yet')
        # the times are not sorted
        # idea: if the new time is outside of computed range, then add on dW
        # otherwise, interpolate via Brownian bridge for the adjacent times
        # that have been computed already
        # W = [0.0]

# might define some Kernel density functions that are consistent with
#   scipy.stats.gaussian_kde()
        



