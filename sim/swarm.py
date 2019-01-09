# -*- coding: utf-8 -*-
"""
Created on Mon Jan 07 18:58:44 2019

@author: sarah
"""
import collections as collections

drone = collections.namedtuple("drone", "x y vx vy");
class drone:
    def __init__(self, xInd, yInd, xIndMax, yIndMax, resolution):
        self.XMax = xIndMax;
        self.YMax = yIndMax;
        self.xInd = xInd;
        self.yInd = yInd;
        self.vx = 0;
        self.vy = 0;
        self.resolution = resolution;
        
    def x(self):
        return self.xInd *self.resolution;
    
    def y(self):
        return self.yInd *self.resolution;
    
    def increment(self, velX, velY): 
        # given current velocity, increment current x/y indices
        xPos = self.x() + velX;
        yPos = self.y() + velY;
#        print xPos, "  ", yPos;
        self.vx = velX; 
        self.vy = velY;
#        print int(xPos/self.resolution), "  ",  int(yPos/self.resolution);
        self.xInd = int(round(xPos/self.resolution)); 
        self.yInd = int(round(yPos/self.resolution));
        
    def __setattr__(self, name, value): 
        if name == "xInd":
            value =  max( min(self.XMax, value), 0);
        elif name == "yInd": 
            value = max( min(self.YMax, value), 0);
        self.__dict__[name] = value;  
          
def moveSwarm(swarmPlot, velField, VX, VY, swarm):
    swarmPlot.remove();
    for drone in swarm:
        drone.increment(VX[drone.yInd,drone.xInd], VY[drone.yInd,drone.xInd]);
    newSwarm = showSwarm(swarm, velField);    
    return newSwarm;

def showSwarm(swarm, velField):
    swarmX = []; swarmY = [];
    for drone in swarm:
        swarmX.append(drone.x());
        swarmY.append(drone.y());
#    print swarmX;
#    print swarmY;
    newPos = velField.scatter(swarmX, swarmY, color='r', s=15);
    return newPos;