# -*- coding: utf-8 -*-
"""
Created on Mon Jan 07 19:02:33 2019

@author: sarah
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.animation as manimation
import matplotlib.pyplot as plt
import numpy as np
import velocityFields as vf
import swarm as sw
import est.Gaussian as est
"""
===========
MovieWriter
===========

This example uses a MovieWriter directly to grab individual frames and write
them to a file. This avoids any event loop integration, but has the advantage
of working with even the Agg backend. This is not recommended for use in an
interactive setting.

"""
def makeMovie(X,Y, U,V, swarm, Time, kernel = False):
    FFMpegWriter = manimation.writers['ffmpeg']
    metadata = dict(title='Movie Test', artist='Matplotlib',
                    comment='Movie support!');
    writer = FFMpegWriter(fps=15, metadata=metadata)
    
    fig, velField = vf.showField(X,Y,U,V, returnHandle =True);
    swarmPlot  = sw.showSwarm(swarm,velField);
    targDrone = swarm[0];
    with writer.saving(fig, "swarm_sim_density.mp4", 100):
        for i in range(Time):
            nSwarmPlot = sw.moveSwarm(swarmPlot, velField, U,V, swarm);
            if kernel:
                neighbours = est.nearestNeighbours(swarm, targDrone, 1.0);
                points = np.zeros((2, len(neighbours)));
                for ind in xrange(len(neighbours)):
                    points[:,ind] = neighbours[ind];
                distribution = est.GaussianKde(points,X,Y)       
                velField.imshow(np.flipud(distribution), cmap=plt.cm.gist_earth_r, 
                extent=[0, 2*np.pi, 0, 2*np.pi]);
                                
            swarmPlot = nSwarmPlot;
            writer.grab_frame();
            