# -*- coding: utf-8 -*-
"""
Created on Mon Jan 07 18:17:33 2019

@author: sarah
"""
import sim.makeMovie as mv
import sim.swarm as sw
import numpy as np
#--------------- velocity field definition ---------------#
X, Y = np.meshgrid(np.arange(0, 2 * np.pi, .2), np.arange(0, 2 * np.pi, .2))
U = np.cos(X);
V = np.sin(Y);

##-------------- velocity field base ------------------#
#fig, ax  = vf.showField(X,Y,U,V, returnHandle = True);

#-------------- velocity field base ------------------#
aDrone = sw.drone(0,0,0,0);
swarm = [aDrone];

mv.makeMovie(X,Y,U,V, swarm, 10);

