# -*- coding: utf-8 -*-
"""
Created on Mon Jan 07 19:02:33 2019

@author: sarah
"""
import numpy as np

def velocity(localGaussian, drone, D):
    return D*localGaussian.grad(drone.x, drone.y)/localGaussian.eval(drone.x, drone.y) + np.random.normal(0, 0.02);