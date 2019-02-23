#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 23:41:15 2019

@author: sarahli
"""
import numpy as np
import matplotlib.pyplot as plt
import sim.makeMovie as mv
import scipy.linalg as sl
import cvxpy as cvx

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

#---------------------per scene logistics ----------------------------#
# Generate velocity visualization
swarmX = trajectories[0, :, 0];
swarmY = trajectories[1, :, 0]; 
fig, simAx = plt.subplots();
simAx.set_title("Velocity field visualization");

# initialize velocity and position   
#velField = vf.showVel(swarm, simAx,X,Y, False);
#swarmPlot  = sw.showSwarm(swarm, simAx);
#points = sw.extractPos(swarm);
#distribution = est.GaussianKde(points,X,Y)       
#heatMap = simAx.imshow(np.flipud(distribution), cmap=plt.cm.gist_earth_r, 
#                       extent=[0, xMax, 0, yMax]);
#fig.colorbar(heatMap);  
plt.axis('equal')             
simAx.set_xlim([0, 1]);
simAx.set_ylim([0, 1]);
swarmPlot = simAx.scatter(targets[0,:], targets[1,:], marker='x', color='b', s=30);
swarmPlot = simAx.scatter(swarmX, swarmY, color='r', s=15);

# simulateKernel is called per scene
def simulateKernel(swarmPlot, velField,heatMap,time):
    swarmPlot.remove();
    # update swarmX and swarmY
    
    swarmX = trajectories[0, :, time];
    swarmY = trajectories[1, :, time]; 
    nSwarmPlot = simAx.scatter(swarmX, swarmY, color='r', s=15);
    
    return nSwarmPlot, None, None;

#-------------- show results ------------------#
mv.makeMovie("LP_swarm_Dylan.mp4",fig, swarmPlot, None, None, nt-1, simulateKernel,useTime=True);
plt.close('all');

