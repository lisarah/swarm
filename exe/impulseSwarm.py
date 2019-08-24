# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 14:38:52 2019

@author: Dylan
"""

import numpy as np
import scipy.linalg as sl
import HillMatrix as hm
import cvxpy as cvx
import matplotlib.pyplot as plt
import sim.makeMovie as mv

# The architecture is as follows:
# The initial positions of all swarm agents are known, and there is a set of
#   provided destinations. Each agent should arrive at a unique destination at
#   the end of the maneuver.
# The dynamics take the form dx/dt = A*x(t) + B*u(t), y(t) = C*x(t)

# Step 0: define the problem

d = 2 # number of spatial dimensions
n = 2*d # n is the dimension of the state
m = d # m is the dimension of the input
p = 2 # p is the dimension of the output
rootN = 10
N = rootN**2 # N is the number of agents
Id = np.eye(d, dtype=float)
Od = np.zeros((d, d), dtype=float)
Ip = np.eye(p, dtype=float)
Orest = np.zeros((p, n-p), dtype=float)
Re = 6.3781366e6 # radius of Earth, in meters
h = 3e5 # altitude of orbit, in meters
a = Re + h # orbit radius, in meters
muEarth = 3.986004415e14 # Earth gravitational parameter, in m^3*s^-2
nOrbit = (muEarth/a**3)**0.5 # angular frequency of the orbit, in rad*s^-1
A = hm.HillMatrix(a, d)
B = np.vstack((Od, Id))
C = np.hstack((Ip,Orest))

ti = 0.0
thetaf = 0.51*np.pi # thetaf = n*tf, if thetaf=2*pi then maneuver happens in 1 orbit
tf = thetaf/nOrbit # time at completion of maneuver, in seconds
nt = 101
times = np.linspace(ti, tf, num=nt)
#Ahistory = np.full((n, n, nt), np.NaN)
#Bhistory = np.full((n, m, nt), np.NaN)
#Chistory = np.full((p, n, nt), np.NaN)
#for k in range(nt):
#    Ahistory[:, :, k] = A
#    Bhistory[:, :, k] = B
#    Chistory[:, :, k] = C

# def eAt(t):
#     return sl.expm(A*t)

if d==2:
    modes = np.array([[0.0, -2/(3*nOrbit), 1.0,       0.0   ],
                      [1.0, 0.0,           0.0,       2.0   ],
                      [0.0, 0.0,           0.0,       nOrbit],
                      [0.0, 1.0,           -2*nOrbit, 0.0   ]])
elif d==3:
    modes = np.array([[0.0, -2/(3*nOrbit), 1.0,       0.0,    0.0, 0.0   ],
                      [1.0, 0.0,           0.0,       2.0,    0.0, 0.0   ],
                      [0.0, 0.0,           0.0,       0.0,    1.0, 0.0   ],
                      [0.0, 0.0,           0.0,       nOrbit, 0.0, 0.0   ],
                      [0.0, 1.0,           -2*nOrbit, 0.0,    0.0, 0.0   ],
                      [0.0, 0.0,           0.0,       0.0,    0.0, nOrbit]])

xvalues = np.linspace(-1.0,1.0,num=rootN)
onesvector = np.ones(rootN)
rn = np.random.rand(2,N)
rn0 = np.zeros((2,N))
for j in range(N):
    rn0[0, j] = np.cos(2*np.pi*rn[1,j])*rn[0,j]**0.5
    rn0[1, j] = np.sin(2*np.pi*rn[1,j])*rn[0,j]**0.5
x0 =  modes[:, 2:4].dot(rn0) # initial states
xf = modes[:, 2:4].dot( np.vstack(( np.kron(xvalues,onesvector), np.kron(onesvector,xvalues) )) )
# x0 = xf
# xf = modes[:, 2:4].dot(np.random.randn(2,N)) # random target states, in the elliptical motion mode


# now compute the cost matrix: Costs[i,j] = cost to send agent i to target j
Costs = np.full((N, N), np.Inf) # initialize with infinite cost everywhere
expAdt = sl.expm(A*(tf - ti))
blockmat = np.linalg.inv(np.block([[expAdt[:d,d:], np.zeros((d,d))], [expAdt[d:,d:], np.eye(d)]]))
for i in range(N):
    for j in range(N):
        deltaV0 = np.linalg.norm(blockmat[:d,:].dot(xf[:,j] - expAdt.dot(x0[:,i])), ord=2)
        deltaVf = np.linalg.norm(blockmat[d:,:].dot(xf[:,j] - expAdt.dot(x0[:,i])), ord=2)
        Costs[i,j] = deltaV0 + deltaVf



# Find the optimal place for each agent to go

Ydual = cvx.Variable((N, N))
objective = cvx.Minimize(cvx.trace(Costs.T*Ydual))
onesNAgent = np.ones(N);
onesNTarg = np.ones(N);
# send each agent to a unique target
constraints = [
        Ydual >= 0,
        Ydual*onesNTarg == onesNAgent,
        onesNAgent*Ydual == onesNTarg
        ]
theProgram = cvx.Problem(objective, constraints)
theProgram.solve(solver='SCS', verbose=False)
Yopt = Ydual.value
# Y[i,j] = 1 iff agent i is instructed to go to target j
dests = [] # dests[i] will be the target assigned to agent i
for i in range(N):
    ji = np.argmax(Yopt[i, :])
    dests.append(ji)
    Yopt[:, ji] = -np.inf

# Now generate the optimal trajectories for each agent

v0plus = np.zeros((d, N))
for i in range(N):
    xfj = xf[:d, dests[i]]
    v0plus[:, i] = np.linalg.inv(expAdt[:d, d:]).dot( xfj - expAdt[:d, :d].dot(x0[:d, i]))

x0plus = np.vstack((x0[:d, :], v0plus))



X = np.full((2*d, N, nt), np.nan)
Y = np.full((d, N, nt), np.nan)

for k in range(nt):
    tk = times[k]
    eAtk = sl.expm(A*(tk-ti))
    for i in range(N):
        Xik = eAtk.dot(x0plus[:,i])
        X[:, i, k] = Xik
        Y[:, i, k] = C.dot(Xik)

# Now make the swarm animation

swarmX = Y[0, :, 0];
swarmY = Y[1, :, 0]; 
fig, simAx = plt.subplots();
simAx.set_title("Impulse-Controlled Swarm");

# plt.axis('equal')
simAx.set_xlim([-3, 3]);
simAx.set_ylim([-3, 3]);

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
mv.makeMovie("Impulse_Swarm_01.mp4", fig, swarmPlot, None, None, nt-1, simulateKernel, useTime=True);
plt.close('all');