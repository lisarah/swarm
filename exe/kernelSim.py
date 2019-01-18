#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 17:29:41 2019

@author: sarahli
"""
import numpy as np
import random as rn
import sim.swarm as sw
import est.Gaussian as est
import matplotlib.pyplot as plt
import sim.velocityFields as vf
import sim.makeMovie as mv
#--------------- velocity field definition ---------------#
xMax = 2 * np.pi; yMax = 2 * np.pi; resolution = 0.2;
X, Y = np.meshgrid(np.arange(0, xMax, resolution), np.arange(0, yMax, resolution));
speedFactor = 2.5;
U = np.cos(X)/speedFactor;
V = np.sin(Y)/speedFactor;
xIndMax, yIndMax = X.shape;

#-------------- add drones ------------------#
droneNum = 40;
swarm = [];
print " Initial Positions ";
for d in range(droneNum):
    xInit = rn.randint(0, xIndMax); yInit = rn.randint(0, yIndMax);
    print xInit, "  ", yInit;
    swarm.append(sw.drone(xInit, yInit, 
                          xIndMax - 1, yIndMax - 1, resolution, d+1));
                          
#-------------- gaussian estimation ------------------#
targDrone = swarm[0];
neighbours = est.nearestNeighbours(swarm, targDrone, 1.0);
points = np.zeros((2, len(neighbours)));
for ind in xrange(len(neighbours)):
    points[:,ind] = neighbours[ind];
#points = sw.extractPos(swarm);
distribution = est.GaussianKde(points,X,Y)        
targDrone = swarm[0];
#---------------------per scene logistics ----------------------------#
fig, simAx = vf.showField(X,Y,U,V, returnHandle =True);
swarmPlot  = sw.showSwarm(swarm,simAx);

def simulateKernel(swarmPlot, a, b):
    nSwarmPlot = sw.moveSwarm(swarmPlot, simAx, swarm);
    neighbours = est.nearestNeighbours(swarm, targDrone, 1.0);
    points = np.zeros((2, len(neighbours)));
    for ind in xrange(len(neighbours)):
        points[:,ind] = neighbours[ind];
    distribution = est.GaussianKde(points,X,Y)       
    simAx.imshow(np.flipud(distribution), cmap=plt.cm.gist_earth_r, 
    extent=[0, 2*np.pi, 0, 2*np.pi]);                    
    return nSwarmPlot, a, b;

#-------------- show results ------------------#
mv.makeMovie("swarm_sim_kernel.mp4", fig, swarmPlot, None, None, 30, simulateKernel);
plt.close('all');
#fig, velField = vf.showField(X,Y,U,V, returnHandle =True);            
#velField.imshow(np.flipud(distribution), cmap=plt.cm.gist_earth_r, 
#                extent=[0, xMax, 0, yMax])
#swarmPlot  = sw.showSwarm(swarm,velField);
#velField.set_xlim([0, xMax])
#velField.set_ylim([0, yMax])
#plt.show()
#   
