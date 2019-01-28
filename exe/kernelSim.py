#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 17:29:41 2019

@author: sarahli
"""
import numpy as np
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
swarm = sw.initSwarm(xMax, yMax, xIndMax, yIndMax, resolution, num= 40, verbose = False);
                          
#-------------- gaussian estimation ------------------#
targDrone = swarm[0];
neighbours = est.nearestNeighbours(swarm, targDrone, 1.0);
distribution = est.GaussianKde(neighbours,X,Y, isSwarm = True)        

#---------------------per scene logistics ----------------------------#
fig, simAx = vf.showField(X,Y,U,V, returnHandle =True);
swarmPlot  = sw.showSwarm(swarm,simAx);

def simulateKernel(swarmPlot, a, b):
    # move drones according to current velocity
    nSwarmPlot = sw.moveSwarm(swarmPlot, simAx, swarm);
    # find neighbours of target drone
    neighbours = est.nearestNeighbours(swarm, targDrone, 1.0);
    # use off the shelf gaussian kernel to estimate distribtuion
    distribution = est.GaussianKde(neighbours,X,Y,isSwarm = True)  
    # show heatmap     
    simAx.imshow(np.flipud(distribution), cmap=plt.cm.gist_earth_r, 
    extent=[0, xMax, 0, yMax]);   
                 
    return nSwarmPlot, a, b;

#-------------- show results ------------------#
mv.makeMovie("swarm_sim_kernel.mp4", fig, swarmPlot, None, None, 30, simulateKernel);
plt.close('all');
