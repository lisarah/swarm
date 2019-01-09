# -*- coding: utf-8 -*-
"""
Created on Mon Jan 07 19:02:33 2019

@author: sarah
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as manimation

import velocityFields as vf
import swarm as sw
"""
===========
MovieWriter
===========

This example uses a MovieWriter directly to grab individual frames and write
them to a file. This avoids any event loop integration, but has the advantage
of working with even the Agg backend. This is not recommended for use in an
interactive setting.

"""

def makeMovie(X,Y, U,V, swarm, Time):

    FFMpegWriter = manimation.writers['ffmpeg']
    metadata = dict(title='Movie Test', artist='Matplotlib',
                    comment='Movie support!');
    writer = FFMpegWriter(fps=15, metadata=metadata)
    
    fig, velField = vf.showField(X,Y,U,V, returnHandle =True);
    swarmPlot  = sw.showSwarm(swarm,velField);

    
    with writer.saving(fig, "writer_test.mp4", 100):
        for i in range(Time):
            nSwarmPlot = sw.moveSwarm(swarmPlot, velField, U,V, swarm);
            swarmPlot = nSwarmPlot;
            writer.grab_frame();
            