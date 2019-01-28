# -*- coding: utf-8 -*-
"""
Created on Mon Jan 07 19:02:33 2019

@author: sarah
"""


def velocity(localGaussian, drone, D):
    return D*localGaussian.grad(drone.x, drone.y)/localGaussian.eval(drone.x, drone.y);

