# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 16:56:57 2019

@author: Dylan
"""

import numpy as np
import scipy.linalg as sl
import matplotlib.pyplot as plt
import sim.makeMovie as mv

Re = float(6.3781366e6) # equatorial radius of Earth, in meters
h = float(3e5) # altitude of orbit, in meters
mu = float(3.986004415e14) # Earth gravitational parameter, in m^3*s^-2
a = Re + h # radius of the nominal circular orbit, in meters
n = (mu/a**3)**0.5 # angular frequency of the orbit, in m*s^-1
Nagents = 100 # number of agents in the swarm
d = 2 # spatial dimension (d=2 if planar motion, d=3 if general motion)
t0 = 0.0 # time at start of maneuver, in seconds
thetaf = 8*np.pi # thetaf = n*tf, if thetaf=2*pi then maneuver happens in 1 orbit
tf = thetaf/n # time at completion of maneuver, in seconds
nt = 201 # number of time steps from start to finish
times = np.linspace(t0, tf, num=nt)


Od = np.zeros([d, d])
Id = np.eye(d)
if d==2:
    Avr = np.array([[3*n**2, 0],
                    [0,      0]])
    Avv = np.array([[0,    2*n],
                    [-2*n, 0  ]])
elif d==3:
    Avr = np.array([[3*n**2, 0, 0    ],
                    [0,      0, 0    ],
                    [0,      0, -n**2]])
    Avv = np.array([[0,    2*n, 0],
                    [-2*n, 0,   0],
                    [0,    0,   0]])
A = np.block([[Od, Id],
              [Avr, Avv]])
B = np.vstack((Od, Id))
C = np.hstack((Id, Od))

# The linearized orbital dynamics are dx/dt = A*x + B*u, y = C*x


x0 = np.random.randn(d, Nagents)
# v0 = np.array([[0, n/2], [-2*n, 0]]).dot(x0)
v0 = 2*n*np.random.randn(d, Nagents)
X0 = np.vstack((x0, v0))
X = np.full((2*d, Nagents, nt), np.nan)
Y = np.full((d, Nagents, nt), np.nan)

for k in range(nt):
    tk = times[k]
    eAtk = sl.expm(A*(tk-t0))
    for i in range(Nagents):
        Xik = eAtk.dot(X0[:,i])
        X[:, i, k] = Xik
        Y[:, i, k] = C.dot(Xik)

# Now make the swarm animation

swarmX = Y[0, :, 0];
swarmY = Y[1, :, 0]; 
fig, simAx = plt.subplots();
simAx.set_title("Hill's Equations Demo");

# plt.axis('equal')
simAx.set_xlim([-100, 100]);
simAx.set_ylim([-100, 100]);

swarmPlot = simAx.scatter(swarmX, swarmY, color='r', s=15);

# simulateKernel is called per scene
def simulateKernel(swarmPlot, velField, heatMap, time):
    swarmPlot.remove();
    # update swarmX and swarmY
    
    swarmX = Y[0, :, time];
    swarmY = Y[1, :, time]; 
    nSwarmPlot = simAx.scatter(swarmX, swarmY, color='r', s=15);    
    return nSwarmPlot, None, None;

#-------------- show results ------------------#
mv.makeMovie("Hill_Demo.mp4", fig, swarmPlot, None, None, nt-1, simulateKernel, useTime=True);
plt.close('all');