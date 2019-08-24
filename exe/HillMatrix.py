# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:01:29 2019

@author: Dylan
"""
import numpy as np

# The linearized dynamics of a circular orbit of radius "a" around Earth is
# dx/dt = A*x, where x = [[rlocal], [vlocal]] is the position and velocity in
# the [[radial], [transverse], [out-of-plane]] rotating reference frame.


def HillMatrix(a, d, units):
    # "a" is the orbit semimajor axis (radius)
    # "d" is the number of spatial dimensions: 2 for planar motion, 3 for general motion
    # If units=='SI', then use SI units. Otherwise, normalize muEarth==1.
    if units == 'SI':
        # Re = 6.3781366e6  # equatorial radius of Earth, in meters
        muEarth = 3.986004415e14 # Earth gravitational parameter, in m^3*s^-2
    elif units == 'normalized':
        muEarth = 1.0
        
    n = (muEarth/a**3)**0.5 # angular frequency of the orbit
    Od = np.zeros([d, d])
    Id = np.eye(d)
    if d==2:
        Avr = np.array([[3*n**2, 0],
                        [0,      0]])
        Avv = np.array([[0,      2*n],
                        [-2*n,   0  ]])
    elif d==3:
        Avr = np.array([[3*n**2, 0, 0    ],
                        [0,      0, 0    ],
                        [0,      0, -n**2]])
        Avv = np.array([[0,    2*n, 0],
                        [-2*n, 0,   0],
                        [0,    0,   0]])
        
    A = np.block([[Od,  Id],
                  [Avr, Avv]])
    return A
