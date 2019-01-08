# -*- coding: utf-8 -*-
"""
Created on Mon Jan 07 18:17:33 2019

@author: sarah
"""
import sim.velocityFields as vf
import numpy as np
X, Y = np.meshgrid(np.arange(0, 2 * np.pi, .2), np.arange(0, 2 * np.pi, .2))
U = np.cos(X)
V = np.sin(Y)
fig, ax  = vf.showField(X,Y,U,V, returnHandle = True);