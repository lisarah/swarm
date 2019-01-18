#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 23:41:15 2019

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
xIndMax, yIndMax = X.shape;
#U = np.cos(X)/speedFactor;
#V = np.sin(Y)/speedFactor;


#-------------- add drones ------------------#
droneNum = 100;
swarm = [];
print " Initial Positions ";
for d in range(droneNum):
    xInit = rn.randint(0, xIndMax/3); yInit = rn.randint(0, yIndMax/3);
    print xInit, "  ", yInit;
    swarm.append(sw.drone(xInit, yInit, 
                          xIndMax - 1, yIndMax - 1, resolution, d+1));
                          
#-------------- gaussian estimation ------------------#
#targDrone = swarm[0];
#neighbours = est.nearestNeighbours(swarm, targDrone, 1.0);
#points = np.zeros((2, len(neighbours)));
#for ind in xrange(len(neighbours)):
#    points[:,ind] = neighbours[ind];
##points = sw.extractPos(swarm);
#distribution = est.GaussianKde(points,X,Y)        

#---------------------per scene logistics ----------------------------#
# Generate velocity visualization
fig, simAx = plt.subplots();
simAx.set_title("Velocity field visualization");
velField = vf.showVel(swarm, simAx,X,Y, False);
swarmPlot  = sw.showSwarm(swarm, simAx);

def simulateKernel(swarmPlot, velField):
        
    nSwarmPlot = sw.moveSwarm(swarmPlot, simAx, swarm);
    nVelField = vf.updateVel(velField, simAx, X,Y,swarm);
    simAx.set_xlim([0, xMax])
    simAx.set_ylim([0, yMax])
#    neighbours = est.nearestNeighbours(swarm, targDrone, 1.0);
#    points = np.zeros((2, len(neighbours)));
#    for ind in xrange(len(neighbours)):
#        points[:,ind] = neighbours[ind];
#    distribution = est.GaussianKde(points,X,Y)    
#    simAx.imshow(np.flipud(distribution), cmap=plt.cm.gist_earth_r, 
#    extent=[0, 2*np.pi, 0, 2*np.pi]);                    
    return nSwarmPlot, nVelField;

#-------------- show results ------------------#
mv.makeMovie(fig, swarmPlot, velField, 30, simulateKernel);
plt.close('all');
#fig, velField = vf.showField(X,Y,U,V, returnHandle =True);            
#velField.imshow(np.flipud(distribution), cmap=plt.cm.gist_earth_r, 
#                extent=[0, xMax, 0, yMax])
#swarmPlot  = sw.showSwarm(swarm,velField);
#velField.set_xlim([0, xMax])
#velField.set_ylim([0, yMax])
#plt.show()
#   
