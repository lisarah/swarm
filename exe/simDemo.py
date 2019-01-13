# -*- coding: utf-8 -*-
"""
Created on Mon Jan 07 18:17:33 2019

@author: sarah
"""
import sim.makeMovie as mv
import sim.swarm as sw
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
droneNum = 20;
swarm = [];
print " Initial Positions ";
for d in range(droneNum):
    xInit = rn.randint(0, xIndMax); yInit = rn.randint(0, yIndMax);
    print xInit, "  ", yInit;
    swarm.append(sw.drone(xInit, yInit, 
                          xIndMax - 1, yIndMax - 1, resolution));
    
#-------------- make movie ------------------#
mv.makeMovie(X,Y,U,V, swarm, 30);
plt.close('all');