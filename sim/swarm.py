# -*- coding: utf-8 -*-
"""
Created on Mon Jan 07 18:58:44 2019

@author: sarah
"""
import collections as collections

drone = collections.namedtuple("drone", "x y vx vy");
class drone:
    x = 0; y = 0; vx = 0; vy = 0;
    def __init__(self, xInd, yInd, vx, vy):
        self.xInd = xInd;
        self.yInd = yInd;
        self.vx = vx;
        self.vy = vy;
        
def moveSwarm(swarmPlot, velField, X, Y, VX, VY, swarm):
    swarmPlot.remove();
    XMax, YMax = X.shape;
    for drone in swarm:
        print drone.x, "  ", drone.y; 
        # need a drone index function
        drone.vx += VX[int(drone.x), int(drone.y)];
        drone.vy += VY[int(drone.x), int(drone.y)];
        drone.x += drone.vx;
        drone.y += drone.vy;
        if drone.x > X[XMax - 1]:
            drone.x = X[XMax - 1];
        elif drone.x < 0:
            drone.x = 0;
        if drone.y >  Y[YMax - 1]:
            drone.y = YMax - 1.;
        elif drone.y < 0:
            drone.y = 0;            
    newSwarm = showSwarm(swarm, velField);    
    return newSwarm;

def showSwarm(swarm, velField):
    swarmX = []; swarmY = [];
    for drone in swarm:
        swarmX.append(drone.x);
        swarmY.append(drone.y);
    newPos = velField.scatter(swarmX, swarmY, color='r', s=10);
    return newPos;