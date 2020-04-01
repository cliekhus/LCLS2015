# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:58:50 2020

@author: chels
"""


import numpy as np
import os
import matplotlib.pyplot as plt

ii = 5

holedensity = [.10, .21, .36, .50, .60, .75, .84]

file = os.getcwd()+'\\simulation\\feru-series-2-'

Croots = np.empty((95, len(holedensity)))
Camps = np.empty((95, len(holedensity)))

for ii in range(len(holedensity)):
    calc = np.loadtxt(file+str(int(holedensity[ii]*100))+'.dat')
    roots = np.loadtxt(file+str(int(holedensity[ii]*100))+'.roots')
    
    Croots[:,ii] = roots[5:, 0]
    Camps[:,ii] = roots[5:, 1]

plt.figure()

for ii in range(20):
    plt.plot(holedensity, Croots[ii,:], marker = 'o')
    
    
#plt.figure()

#for ii in range(95):
#    plt.plot(holedensity, Camps[ii,:])