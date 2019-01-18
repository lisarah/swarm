# -*- coding: utf-8 -*-
"""
Created on Mon Jan 07 18:58:44 2019

@author: sarah
"""
import collections as collections
import numpy as np
import math as math

drone = collections.namedtuple("drone", "x y vx vy");
class drone:
    def __init__(self, xInd, yInd, xIndMax, yIndMax, resolution, did = 0):
        self.XMax = xIndMax;
        self.YMax = yIndMax;
        self.xInd = xInd;
        self.yInd = yInd;
        self.vx = 0;
        self.vy = 0;
        self.resolution = resolution;
        self.id = did;
    def x(self):
        return self.xInd *self.resolution;
    
    def y(self):
        return self.yInd *self.resolution;
    
    def increment(self): 
        # given current velocity, increment current x/y indices
        xPos = self.x() + self.vx;
        yPos = self.y() + self.vy;
#        print int(xPos/self.resolution), "  ",  int(yPos/self.resolution);
        self.xInd = int(round(xPos/self.resolution)); 
        self.yInd = int(round(yPos/self.resolution));
        
    def __setattr__(self, name, value): 
        if name == "xInd":
            value =  max( min(self.XMax, value), 0);
        elif name == "yInd": 
            value = max( min(self.YMax, value), 0);
        self.__dict__[name] = value;  
    def distance(self, drone):
        return math.hypot(self.x() - drone.x(), self.y() - drone.y());
          
def moveSwarm(swarmPlot, simAx, swarm):
    swarmPlot.remove();
    for drone in swarm:
        drone.increment();
    newSwarm = showSwarm(swarm, simAx);    
    return newSwarm;

def showSwarm(swarm, simAx):
    swarmX = []; swarmY = [];
    for drone in swarm:
        swarmX.append(drone.x());
        swarmY.append(drone.y());

    newPos = simAx.scatter(swarmX, swarmY, color='r', s=15);

    return newPos;

def extractPos(swarm):
    dataNum =  len(swarm);
    points= np.zeros((2, dataNum));
    droneIter = 0;

    for drone in swarm:
        points[0, droneIter] = drone.x();
        points[1, droneIter] = drone.y();
        droneIter +=1;
    return points;
    
    
    
    
    