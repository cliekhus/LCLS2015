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
colorchoice = ['k', 'c', 'g', 'r', 'm', 'y', 'b']
linechoice = ['-', ':', '--', '-.']

file = os.getcwd()+'\\simulation\\feru-series-2-'

Croots = np.empty((95, len(holedensity)))
Camps = np.empty((95, len(holedensity)))

for ii in range(len(holedensity)):
    calc = np.loadtxt(file+str(int(holedensity[ii]*100))+'.dat')
    roots = np.loadtxt(file+str(int(holedensity[ii]*100))+'.roots')
    
    Croots[:,ii] = roots[5:, 0]
    Camps[:,ii] = roots[5:, 1]

plt.figure(figsize = (7.5,8))

for ii in range(len(colorchoice)*len(linechoice)):
    plt.plot(holedensity, Croots[ii,:], color = colorchoice[ii%len(colorchoice)], linestyle = linechoice[ii//len(colorchoice)], label = 'root {}'.format(ii))
    for jj in range(len(holedensity)):
        plt.scatter(holedensity[jj], Croots[ii,jj], s = Camps[ii,jj]*100000000, color = colorchoice[ii%len(colorchoice)], alpha = 0.3)
    
plt.legend()
plt.xlim([0,1.2])
plt.xlabel('Fe hole charge')
plt.ylabel('unshifted C peak energy (eV)')
#plt.figure()

#for ii in range(95):
#    plt.plot(holedensity, Camps[ii,:])