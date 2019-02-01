# -*- coding: utf-8 -*-
"""
Created on Mon Jan 07 19:02:33 2019

@author: sarah
"""
import numpy as np
import scipy.stats as st

def densityGen():
    totalDensity = [];
    gaussians = [np.array([np.pi, np.pi])];
#    gaussians = [np.array([np.pi/3, 5*np.pi/3]),
#                 np.array([5*np.pi/3, 5*np.pi/3]),
#                 np.array([np.pi/3, np.pi/2]),
#                 np.array([3*np.pi/4, 2.5*np.pi/6]),
#                 np.array([np.pi, np.pi/3]),
#                 np.array([5*np.pi/4, 2.5*np.pi/6]),
#                 np.array([5*np.pi/3, np.pi/2])];
    for gauss in gaussians:
        totalDensity.append(st.multivariate_normal(mean=gauss, cov =1.0 *np.eye(2)));
    return totalDensity;

def velocity(localGaussian, drone, D, desiredDensity = None):
    offSet = np.zeros(2);
    if desiredDensity is not None:
        offSet = desiredDensity.grad(drone.x, drone.y);
        
    return D*(localGaussian.grad(drone.x, drone.y) - offSet)/localGaussian.eval(drone.x, drone.y) + np.random.normal(0, 0.01);