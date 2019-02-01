# -*- coding: utf-8 -*-
"""
Created on Mon Jan 07 18:58:44 2019

@author: sarah
"""
import numpy as np
import math as math
import random as rn
class drone:
#    def __init__(self, xInd, yInd, xIndMax, yIndMax, resolution, did = 0):
#        self.XMax = xIndMax;
#        self.YMax = yIndMax;
#        self.xInd = xInd;
#        self.yInd = yInd;
#        self.vx = 0;
#        self.vy = 0;
#        self.resolution = resolution;
#        self.id = did;
        
    def __init__(self, x, y, xMax, yMax, resolution, did = -10):
        self.xMax = xMax;
        self.yMax = yMax;
        self.x = x;
        self.y = y;
        self.vx = 0;
        self.vy = 0;
        self.resolution = resolution;
        self.id = did;
        
    def xInd(self):
        if int(self.x/self.resolution) > 32:
            print "exceeded";
        return int(self.x/self.resolution);
    
    def yInd(self):
        if int(self.x/self.resolution) > 32:
            print "exceeded";
        return int(self.y/self.resolution);
    
    def increment(self): 
        # given current velocity, increment current x/y indices
        self.x = self.x + self.vx;
        self.y = self.y + self.vy;  
        
    def __setattr__(self, name, value): 
        if name == "x":
            value =  max( min(self.__dict__['xMax'], value), 0);
        elif name == "y": 
            value = max( min(self.__dict__['yMax'], value), 0);
        self.__dict__[name] = value;  
        
    def distance(self, drone):
        return math.hypot(self.x - drone.x, self.y - drone.y);
          
def moveSwarm(swarmPlot, simAx, swarm):
    swarmPlot.remove();
    for drone in swarm:
        drone.increment();
    newSwarm = showSwarm(swarm, simAx);    
    return newSwarm;

def showSwarm(swarm, simAx):
    swarmX = []; swarmY = [];
    for drone in swarm:
        swarmX.append(1.0*drone.x);
        swarmY.append(1.0*drone.y);

    newPos = simAx.scatter(swarmX, swarmY, color='r', s=15);

    return newPos;

def extractPos(swarm):
    dataNum =  len(swarm);
    points= np.zeros((2, dataNum));
    droneIter = 0;
    for drone in swarm:
        points[0, droneIter] = drone.xInd();
        points[1, droneIter] = drone.yInd();
        droneIter +=1;
    return points;
    
def initSwarm(xMax, yMax, xIndMax, yIndMax, resolution, num = 10, verbose = True):
    swarm = [];
    if verbose:
        print " Initial Positions ";
    for d in range(num):
        xInit = rn.uniform(0, xMax); yInit = rn.uniform(0, yMax);
        if verbose:
            print xInit, "  ", yInit;
        swarm.append(drone(xInit, yInit, xMax, yMax, resolution, d));
    return swarm;
    
    
    
    