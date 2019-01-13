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
#--------------- velocity field definition ---------------#
xMax = 2 * np.pi; yMax = 2 * np.pi; resolution = 0.2;
X, Y = np.meshgrid(np.arange(0, xMax, resolution), np.arange(0, yMax, resolution));
speedFactor = 2.5;
U = np.cos(X)/speedFactor;
V = np.sin(Y)/speedFactor;
xIndMax, yIndMax = X.shape;

#-------------- add drones ------------------#
droneNum =40;
swarm = [];
print " Initial Positions ";
for d in range(droneNum):
    xInit = rn.randint(0, xIndMax); yInit = rn.randint(0, yIndMax);
    print xInit, "  ", yInit;
    swarm.append(sw.drone(xInit, yInit, 
                          xIndMax - 1, yIndMax - 1, resolution));
#-------------- gaussian estimation ------------------#
points = sw.extractPos(swarm);
distribution =est.GaussianKde(points,X,Y)        


#-------------- show results ------------------#
fig, velField = vf.showField(X,Y,U,V, returnHandle =True);            
velField.imshow(np.flipud(distribution), cmap=plt.cm.gist_earth_r, 
                extent=[0, xMax, 0, yMax])
swarmPlot  = sw.showSwarm(swarm,velField);
velField.set_xlim([0, xMax])
velField.set_ylim([0, yMax])
plt.show()
   
#------------------alternative visualization method under investigation----#
# [https://stackoverflow.com/a/37334212/1595060](https://stackoverflow.com/a/37334212/1595060)
#cmap = plt.get_cmap('Reds')
#my_cmap = cmap(np.arange(cmap.N))
#my_cmap[:, -1] = np.linspace(0, 1, cmap.N)
#my_cmap = ListedColormap(my_cmap)
#
#ax = plt.axes(projection=crs)
#ax.stock_img()
#ax.imshow(v, origin='lower',
#          extent=[x0, x1, y0, y1],
#          interpolation='bilinear',
#          cmap=my_cmap)
#
#plt.show();