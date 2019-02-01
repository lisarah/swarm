#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 20:48:41 2019

@author: sarahli
"""
import numpy as np
import scipy.linalg as sl
#---------------- 2D integrator -----------------------------#
dim = 2; 
T = 0.01;
A = np.zeros((dim*2, dim*2)); B = np.zeros((dim*2, dim));
A[dim, 0] = 1.; A[dim+1, 1 ] = 1.; B[0,0] = 1.; B[1,1] = 1.; 
bigM = np.zeros((dim*3, dim*3));
bigM[0:dim*2, 0:dim*2] = A;
bigM[0:dim*2, 0:dim] = B;

dBigM  = sl.expm(bigM);
dA = dBigM[0:dim*2, 0:dim*2]; 
dB = dBigM[0:dim*2, 0:dim*2];
