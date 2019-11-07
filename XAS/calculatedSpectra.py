# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 16:28:53 2019

@author: chelsea
"""

from numpy import loadtxt
import os
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import matplotlib.patches as pat
import numpy as np

Eoff = 143.6

ploton = True

file = os.getcwd()+'\\simulation\\feru-series-fe-'

holedensity = [0, .40, .55, .72, .77, .86, 1.00]
colorchoice = ['k', 'r', 'b', 'c', 'm', 'y', 'g']


if ploton:
    plt.figure()

def makeABpeak(Eoff, calc, roots, ploton, cc, lc):
    
    sig = .5
    
    Apeak = np.min(roots[:,0])+Eoff
    
    x = np.array(calc[:,0])+Eoff
    Broots = np.array(roots[:,0])
    Bamp = np.array(roots[:,1])
    Bamp = Bamp[Broots+Eoff<7116]
    Bamp = np.delete(Bamp, [0])
    
    Broots = Broots[Broots+Eoff<7116]
    Broots = np.delete(Broots, [0])
    Bshape = np.zeros(np.shape(x))
    for root,amp in zip(Broots,Bamp):
        Bshape = Bshape + amp/50*np.exp(-(x-(root+Eoff))**2/sig**2)
    
    Bpeak = x[np.argmax(Bshape)]

    Croots = np.array(roots[:,0])
    Camp = np.array(roots[:,1])
    Camp = Camp[Croots+Eoff>7116]
    Croots = Croots[Croots+Eoff>7116]
    Cshape = np.zeros(np.shape(x))
    for root,amp in zip(Croots,Camp):
        Cshape = Cshape + amp/50*np.exp(-(x-(root+Eoff))**2/sig**2)
    
    Cpeak = x[np.argmax(Cshape)]
    
    if ploton:
        plt.plot(x, Bshape, color = cc, label = lc)
        plt.plot([Apeak,Apeak], [0,5e-7], color = cc)
        plt.plot(x, Cshape, color = cc)
        plt.legend()
        plt.xlim([7109, 7130])
    
    return Apeak, Bpeak, Cpeak

Apeaks = []
Bpeaks = []

for ii in range(len(holedensity)):
    
    calc = loadtxt(file+str(int(holedensity[ii]*100))+'.dat')
    roots = loadtxt(file+str(int(holedensity[ii]*100))+'.roots')
    Apeak, Bpeak, Cpeak = makeABpeak(Eoff, calc, roots, ploton, colorchoice[ii], str(holedensity[ii]))
    
    Apeaks = Apeaks + [Apeak]
    Bpeaks = Bpeaks + [Bpeak]
    

plt.figure(figsize = (4,5))
plt.plot([x-y for x,y in zip(Bpeaks, Apeaks)], holedensity, 'o')
plt.xlabel('A - B peak energy difference')
plt.ylabel('Fe hole density')
#plt.ylim([0,1.2])
#plt.xlim([0,3.5])
plt.tight_layout()

#fig, ax = plt.subplots(figsize = (4,5))
#patch = pat.Ellipse((ParamsDiff[5]-ParamsDiff[2],.826), 0.2, 0.03, color='r')
#ax.add_patch(patch)
#plt.plot([Bpeak40-Apeak40-Eoff,Bpeak77-Apeak77-Eoff,Bpeak86-Apeak86-Eoff,Bpeak100-Apeak100-Eoff]\
#            ,[.4,.77,.86,1], 'o', linestyle='solid', label = 'calculated')
#plt.xlabel('A - B peak energy difference')
#plt.ylabel('Fe hole density')
#plt.ylim([0,1.2])
#plt.xlim([0,3.5])
#plt.legend()
#plt.tight_layout()





