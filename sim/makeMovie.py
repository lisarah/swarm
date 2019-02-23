# -*- coding: utf-8 -*-
"""
Created on Mon Jan 07 19:02:33 2019

@author: sarah
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.animation as manimation

"""
===========
MovieWriter
===========

This example uses a MovieWriter directly to grab individual frames and write
them to a file. This avoids any event loop integration, but has the advantage
of working with even the Agg backend. This is not recommended for use in an
interactive setting.

"""
def makeMovie(name, fig,  swarmPlot, velField, heatMap, Time, sceneGen = None, useTime = False):
    FFMpegWriter = manimation.writers['ffmpeg']
    metadata = dict(title='Movie Test', artist='Matplotlib',
                    comment='Movie support!');
    writer = FFMpegWriter(fps=20, metadata=metadata)

    with writer.saving(fig, name, 100):
        for i in range(Time):
            if sceneGen != None:
                if useTime:
                    nSwarmPlot,nvelField,nHeatMap = sceneGen(swarmPlot,velField,heatMap,i);#   
                else:
                    nSwarmPlot,nvelField,nHeatMap = sceneGen(swarmPlot,velField,heatMap);#                               
            swarmPlot = nSwarmPlot;
            velField = nvelField;
            heatMap = nHeatMap;
            writer.grab_frame();
            