# -*- coding: utf-8 -*-
"""
Created on Mon Jan 07 18:17:33 2019
Purpose: generate random swarms, 

@author: sarah
"""
import sim.makeMovie as mv
import sim.swarm as sw
import sim.velocityFields as vf
import numpy as np
import random as rn
import matplotlib.pyplot as plt
#--------------- velocity field definition ---------------#
xMax = 2 * np.pi; yMax = 2 * np.pi; resolution = 0.2;
X, Y = np.meshgrid(np.arange(0, xMax, resolution), np.arange(0, yMax, resolution));
speedFactor = 2.5;
U = np.cos(X)/speedFactor;
V = np.sin(Y)/speedFactor;
xIndMax, yIndMax = X.shape;


#-------------- add drones ------------------#
swarm = sw.initSwarm(xMax, yMax, xIndMax, yIndMax, resolution, num = 20)

#---------- per scene logistics ------------#
fig, velField = vf.showField(X,Y,U,V, returnHandle =True);
swarmPlot  = sw.showSwarm(swarm,velField);

def simulateSwarm(swarmPlot,a,b):
    nSwarmPlot = sw.moveSwarm(swarmPlot, velField, swarm);              
    return nSwarmPlot,a,b;
    
#-------------- make movie ------------------#
mv.makeMovie("swarm_sim_demo.mp4", fig, swarmPlot,None,None, 30, simulateSwarm);
plt.close('all');