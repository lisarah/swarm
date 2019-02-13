# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 17:11:01 2019

@author: Dylan
"""


import numpy as np
import scipy.linalg as sl
import cvxpy as cvx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as manimation


d = 2 # number of spatial dimensions
ti = 0.0 # initial time
tf = 1.0 # final time
nt = 101 # number of time steps
Nagents = 40 # number of agents
Ntargets = Nagents # number of targets (should equal Nagents for now)

times = np.linspace(ti, tf, num=nt)
I = np.identity(d, dtype=float)
O = np.zeros((d, d), dtype=float)
# double integrator dynamics: dx/dt = Ax + Bu
A = np.block([[O, I], [O, O]])
B = np.vstack((O, I))
def Wc(t):
    # controllability Gramian for double integrator, found analytically
    tau = t - ti
    return np.block([
            [(tau**3/3.0)*I, (tau**2/2.0)*I],
            [(tau**2/2.0)*I, tau*I]
            ])
    
tdiff = tf - ti
WcfInverse = np.block([
        [(12.0/tdiff**3)*I, (-6.0/tdiff**2)*I],
        [(-6.0/tdiff**2)*I, (4.0/tdiff)*I]
        ]) # inverse of the controllability Gramian over the interval [ti, tf]
# WcfInverse for the double integrator system was found analytically
    
X0 = np.random.rand(d,Nagents) # X0(:,j) is the initial position of agent j
targets = np.random.rand(d,Ntargets) #targets(:,l) is the position of target l
C = np.full((Nagents, Ntargets), np.Inf) # cost of sending agent i to target j
eAtdiff = sl.expm(tdiff*A)
for j in range(Ntargets):
    xvf = np.concatenate((targets[:,j], np.zeros(d)))
    for i in range(Nagents):
        xvi = np.concatenate((X0[:,i], np.zeros(d)))
        xerr = eAtdiff.dot(xvi) - xvf
        C[i,j] = xerr.dot(WcfInverse.dot(xerr))

Y = cvx.Variable((Nagents, Ntargets))
objective = cvx.Minimize(cvx.trace(C.T*Y))
onesNAgent = np.ones(Nagents);
onesNTarg = np.ones(Ntargets);
if Nagents<=Ntargets:
    # send each agent to a unique target
    constraints = [
            Y >= 0,
            Y*onesNTarg == onesNAgent,
            onesNAgent*Y <= onesNTarg
            ]
else:
    # make sure every target is visited by some agent
    constraints = [
            Y >= 0,
            Y*onesNTarg == onesNAgent,
            onesNAgent*Y >= onesNTarg
            ]
theProgram = cvx.Problem(objective, constraints)
theProgram.solve()
Yopt = Y.value
# Y[i,j] = 1 iff agent i is instructed to go to target j
dests = [] # dests[i] will be the target assigned to agent i
for i in range(Nagents):
    dests.append(np.argmax(Yopt[i,:]))

# Now, animate the trajectory
def opttraj(t, xi, xf):
    if t >= tf:
        return xf
    elif t <= ti:
        return xi
    else:
        tau = (t - ti)/(tf - ti)
        return xi + (3*tau**2 - 2*tau**3)*(xf - xi)

trajectories = np.full((d, Nagents, nt), np.NaN)
for j in range(Nagents):
    xi = X0[:, j]
    xf = targets[:, dests[j]]
    k = 0
    for t in times:
        trajectories[:, j, k] = opttraj(t, xi, xf)
        k += 1
# trajectories[:, j, k] is the location of agent j at t=times[k]

FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title='Swarm Movie :)', artist='ACL',
                comment='I hope this works!')
writer = FFMpegWriter(fps=30, metadata=metadata)
fig = plt.figure()
l, = plt.plot([], [], 'k-o')

plt.xlim(-0.1, 1.1)
plt.ylim(-0.1, 1.1)

with writer.saving(fig, "swarm_movie.mp4", nt):
    for k in range(nt):
        l.set_data(trajectories[0, :, k], trajectories[1, :, k], 'ok')
        writer.grab_frame()