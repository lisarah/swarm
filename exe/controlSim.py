#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 23:41:15 2019

@author: sarahli
"""
import numpy as np
import matplotlib.pyplot as plt
import est.Gaussian as est
import sim.swarm as sw
import sim.velocityFields as vf
import sim.makeMovie as mv
#--------------- velocity field definition ---------------#
xMax = 2 * np.pi; yMax = 2 * np.pi; resolution = 0.2;
X, Y = np.meshgrid(np.arange(0, xMax, resolution), np.arange(0, yMax, resolution));
speedFactor = 2.5;
xIndMax, yIndMax = X.shape;
#U = np.cos(X)/speedFactor;
#V = np.sin(Y)/speedFactor;


#-------------- add drones ------------------#
swarm = sw.initSwarm(xMax, yMax, xIndMax, yIndMax, resolution, num = 100)

#---------------------per scene logistics ----------------------------#
# Generate velocity visualization
fig, simAx = plt.subplots();
simAx.set_title("Velocity field visualization");

# initialize velocity and position
velField = vf.showVel(swarm, simAx,X,Y, False);
swarmPlot  = sw.showSwarm(swarm, simAx);
points = sw.extractPos(swarm);
distribution = est.GaussianKde(points,X,Y)       
heatMap = simAx.imshow(np.flipud(distribution), cmap=plt.cm.gist_earth_r, 
                       extent=[0, xMax, 0, yMax]);
fig.colorbar(heatMap);                       
simAx.set_xlim([0, xMax]);
simAx.set_ylim([0, yMax]);

# simulateKernel is called per scene
def simulateKernel(swarmPlot, velField,heatMap):
    heatMap.remove();
    nSwarmPlot = sw.moveSwarm(swarmPlot, simAx, swarm);
    nVelField = vf.updateVel(velField, simAx, X,Y,swarm);
    points = sw.extractPos(swarm);
    distribution = est.GaussianKde(points,X,Y)       
    nheatMap = simAx.imshow(np.flipud(distribution), cmap=plt.cm.gist_earth_r, 
                           extent=[0, xMax, 0, yMax]);                       
    return nSwarmPlot, nVelField, nheatMap;

#-------------- show results ------------------#
mv.makeMovie("swarm_sim_diff.mp4",fig, swarmPlot, velField, heatMap, 30, simulateKernel);
plt.close('all');

