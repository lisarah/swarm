# -*- coding: utf-8 -*-
"""
Created on Mon Jan 07 18:07:33 2019

@author: sarah
"""

import matplotlib.pyplot as plt
import numpy as np


def showField(X, Y, U, V, returnHandle = False):
    fig, ax = plt.subplots()
    ax.set_title("Velocity field visualization")
    M = np.hypot(U, V)
    Q = ax.quiver(X, Y, U, V, M, units='x', pivot='tip', width=0.022,
                   scale=1 / 0.15)
    qk = ax.quiverkey(Q, 0.9, 0.9, 1, r'$1 \frac{m}{s}$', labelpos='E',
                       coordinates='figure')
    plt.show()
    if returnHandle:
        return fig, ax;
    else:
        return;
        
