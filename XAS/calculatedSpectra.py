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
import pickle

Eoff = 143.6

ploton = False

file = os.getcwd()+'\\simulation\\feru-series-2-'

holedensity = [.10, .21, .36, .50, .60, .75, .84]
colorchoice = ['k', 'c', 'g', 'r', 'm', 'y', 'b']
linestyle = ['-', '--', '--', '--', ':', ':', ':']


if ploton:
    plt.figure()

def makeABpeak(Eoff, calc, roots, ploton, cc, lc, ls):
    
    sig = .6
    
    Apeak = np.min(roots[:,0])+Eoff
    Aamp = roots[0,1]
    
    print('Apeak')
    print(Apeak)
    
    x = np.array(calc[:,0])+Eoff
    Broots = np.array(roots[:,0])
    Bamp = np.array(roots[:,1])
    Bamp = Bamp[Broots+Eoff<7116]
    Bamp = np.delete(Bamp, [0])
    
    Broots = Broots[Broots+Eoff<7116]
    #Apeak = Broots[np.argmin(Bamp)]+Eoff
    Broots = np.delete(Broots, [0])
    Bshape = np.zeros(np.shape(x))
    for root,amp in zip(Broots,Bamp):
        Bshape = Bshape + amp*np.exp(-(x-(root+Eoff))**2/sig**2)
    
    #Bpeak = x[np.argmax(Bshape)]
    Bpeak = Broots[np.argmax(Bamp)]+Eoff
    print('Bpeak')
    print(Bpeak)

    Croots = np.array(roots[:,0])
    Camp = np.array(roots[:,1])
    Camp = Camp[Croots+Eoff>7116]
    Croots = Croots[Croots+Eoff>7116]
    Cshape = np.zeros(np.shape(x))
    for root,amp in zip(Croots,Camp):
        Cshape = Cshape + amp*np.exp(-(x-(root+Eoff))**2/sig**2)
    
    Cpeak = x[np.argmax(Cshape)]
    
    if ploton:
        plt.plot(x, Bshape, color = cc, label = lc, linestyle = ls)
        plt.plot(x, Aamp*np.exp(-(x-(Apeak))**2/sig**2), color = cc, linestyle = ls)
        plt.plot(x, Cshape, color = cc, linestyle = ls)
        plt.legend()
        plt.xlim([7109, 7125])
        plt.xlabel('x-ray energy (eV)')
        plt.ylabel('absorption amplitude')
        plt.tight_layout()
    
    return Apeak, Bpeak, Cpeak

Apeaks = []
Bpeaks = []

for ii in range(len(holedensity)):
    
    calc = loadtxt(file+str(int(holedensity[ii]*100))+'.dat')
    roots = loadtxt(file+str(int(holedensity[ii]*100))+'.roots')
    Apeak, Bpeak, Cpeak = makeABpeak(Eoff, calc, roots, ii%3==0, colorchoice[ii], str(holedensity[ii]), linestyle[ii])
    
    Apeaks = Apeaks + [Apeak]
    Bpeaks = Bpeaks + [Bpeak]
    

fig, ax = plt.subplots(figsize = (4,5))
AB = [x-y for x,y in zip(Bpeaks, Apeaks)]
plt.plot(AB, holedensity, 'o', color = '#0072b2', marker = 's', label = 'calculation')
line = np.polyfit(AB, holedensity, 1)
linefit = np.poly1d(line)
plt.plot(AB, linefit(AB), color = 'k')
plt.xlabel('B - A peak energy difference')
plt.ylabel('Fe hole density')
#plt.ylim([0,1.2])
#plt.xlim([0,3.5])
plt.tight_layout()

with open("D://LCLS_Data/LCLS_python_data/XAS_Spectra/BmA.pkl", "rb") as f:
    BmA = pickle.load(f)
with open("D://LCLS_Data/LCLS_python_data/XAS_Spectra/uncertainty.pkl", "rb") as f:
    uncertainty = pickle.load(f)

#fig, ax = plt.subplots(figsize = (4,5))
patch = pat.Ellipse((BmA,linefit(BmA)), 2*uncertainty[1], 2*(linefit(BmA+uncertainty[1])-linefit(BmA-uncertainty[1])), color='#e69f00')
ax.add_patch(patch)
#plt.plot([Bpeak40-Apeak40-Eoff,Bpeak77-Apeak77-Eoff,Bpeak86-Apeak86-Eoff,Bpeak100-Apeak100-Eoff]\
#            ,[.4,.77,.86,1], 'o', linestyle='solid', label = 'calculated')
#plt.xlabel('A - B peak energy difference')
#plt.ylabel('Fe hole density')
plt.ylim([0,1])
plt.xlim([0,3])
plt.plot([-1,-2], [1,2], marker = 'o', label = 'measurement', color = '#e69f00', linestyle = 'none')
#plt.legend()
#plt.tight_layout()
plt.legend()
