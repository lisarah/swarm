# -*- coding: utf-8 -*-
"""
Created on Mon Jan 07 18:07:33 2019

@author: sarah
"""

import matplotlib.pyplot as plt
import numpy as np
import est.Gaussian as est
import control.diffusion as df

def showField(X, Y, U, V, returnHandle = False):
    fig, ax = plt.subplots()
    ax.set_title("Velocity field visualization")
    M = np.hypot(U, V)
    Q = ax.quiver(X, Y, U, V, M, units='x', pivot='mid', width=0.022,
                  scale=0.75)
    qk = ax.quiverkey(Q, 0.9, 0.9, 1, r'$1 \frac{m}{s}$', labelpos='E',
                       coordinates='figure');
    plt.show()
    if returnHandle:
        return fig, ax;
    else:
        return;
        
def updateVel(velField, simAx, X,Y, swarm, visualize = False):
    if visualize:
        velField.remove();
    return showVel(swarm,simAx, X,Y, visualize);  
      
def showVel(swarm, simAx, X,Y, visualize):
    XX, XY = X.shape;
    U = np.zeros((XX,XY));
    V = np.zeros((XX,XY));
    
    for drone in swarm:
        localGauss = est.localGaussian(swarm, drone, 1.0);#last parameter is radius
        vel= df.velocity(localGauss, drone, 0.5);
        U[drone.yInd, drone.xInd] = vel[0];
        V[drone.yInd, drone.xInd] = vel[1];
#        print vel;
        drone.vx = vel[0];
        drone.vy = vel[1];
    if visualize:
        M = np.hypot(U,V);    
        Q = simAx.quiver(X, Y, U, V, M, units='x', pivot='mid', width=0.022,
                       scale=0.75)
        qk = simAx.quiverkey(Q, 0.9, 0.9, 1, r'$1 \frac{m}{s}$', labelpos='E',
                           coordinates='figure')
        plt.show()
        return Q;
    else:
        return None;