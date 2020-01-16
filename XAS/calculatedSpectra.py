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
import matplotlib.gridspec as gridspec
from fitXASDiff import fitXASPiecewiseGauss
from fittingfunctions import lorwslope
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

MinTime = -35
MaxTime = 35

Eoff = 143.6

ploton = False

file = os.getcwd()+'\\simulation\\feru-series-2-'

holedensity = [.10, .21, .36, .50, .60, .75, .84]
colorchoice = ['k', 'c', 'g', 'r', 'm', 'y', 'b']
linestyle = ['-', '--', '--', '--', ':', ':', ':']


if ploton:
    plt.figure()

def makeABpeak(Eoff, calc, roots, ploton, cc, lc, ls, ii, ax2):
    
    sig = .6
    
    Apeak = np.min(roots[:,0])+Eoff
    Aamp = roots[0,1]
    
    print('Apeak')
    print(Apeak)
    
    x = np.array(calc[:,0])+Eoff
    Broots = np.array(roots[:,0])
    Bamp = np.array(roots[:,1])
    Bamp = Bamp[Broots+Eoff<7114]
    Bamp = np.delete(Bamp, [0])
    
    Broots = Broots[Broots+Eoff<7114]
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
    Camp = Camp[Croots+Eoff>=7114]
    Croots = Croots[Croots+Eoff>=7114]
    Cshape = np.zeros(np.shape(x))
    for root,amp in zip(Croots,Camp):
        Cshape = Cshape + amp*np.exp(-(x-(root+Eoff))**2/sig**2)
    
    Cpeak = x[np.argmax(Cshape)]
    
    if ii == 0:
        ax2.plot(x, Bshape+Aamp*np.exp(-(x-(Apeak))**2/sig**2)+Cshape, color = 'k')
        plt.ylabel('absorption amplitude')
        
    if ploton:
        ax1=plt.subplot(2,1,1)
        ax1.plot(x, Bshape, color = cc, label = lc, linestyle = ls)
        ax1.plot(x, Aamp*np.exp(-(x-(Apeak))**2/sig**2), color = cc, linestyle = ls)
        ax1.plot(x, Cshape, color = cc, linestyle = ls)
        ax1.set_xlim([7109, 7125])
        ax1.legend()
        plt.xlabel('x-ray energy (eV)')
        plt.ylabel('absorption amplitude')
        plt.tight_layout()
    
    return Apeak, Bpeak, Cpeak

Apeaks = []
Bpeaks = []

for ii in range(len(holedensity)):
    
    calc = loadtxt(file+str(int(holedensity[ii]*100))+'.dat')
    roots = loadtxt(file+str(int(holedensity[ii]*100))+'.roots')
    
    if ii == 0:
        ax2=plt.subplot(2,1,2)
        ax2.stem(roots[:,0]+Eoff, roots[:,1], colorchoice[0], markerfmt = 'none', label = linestyle[0], linefmt = colorchoice[0]+linestyle[0], basefmt='k')
        ax2.set_xlim([7109, 7125])

    Apeak, Bpeak, Cpeak = makeABpeak(Eoff, calc, roots, ii%3==0, colorchoice[ii], str(holedensity[ii]), linestyle[ii], ii, ax2)
    
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






folder = "D://LCLS_Data/LCLS_python_data/XAS_Spectra/"
        
with open(folder + "XASDiffBootF.pkl", "rb") as f:
    XASDiffBootF = pickle.load(f)
    
with open(folder + "XASDiffBootE.pkl", "rb") as f:
    XASDiffBootE = pickle.load(f)
    
with open(folder + "XASOffBootF.pkl", "rb") as f:
    XASOffBootF = pickle.load(f)
    
with open(folder + "XASOffBootE.pkl", "rb") as f:
    XASOffBootE = pickle.load(f)

with open(folder + "XASOnBootF.pkl", "rb") as f:
    XASOnBootF = pickle.load(f)
        
with open(folder + "xasProData_one.pkl", "rb") as f:
    xasProData_one = pickle.load(f)


Fit,Params,ParamsA,ParamsB,covA,covB = \
        fitXASPiecewiseGauss(xasProData_one.EnergyPlot, XASDiffBootF, XASOffBootF, XASOnBootF, True)
        

pluscolor = '#009E73'
minuscolor = '#0072b2'
pluscolor2 = '#e69f00'

plt.figure(figsize = (4,6))

gridspec.GridSpec(20,1)

ax = plt.subplot2grid((20,1), (0,0), colspan = 1, rowspan = 4)
plt.errorbar(np.delete(xasProData_one.EnergyPlot,-4), np.delete(xasProData_one.XASOff_Norm,-4), np.delete(xasProData_one.Error_Off,-4), color = 'k')
plt.ylabel('$I_{off}$')
ax.set_xticklabels([])
plt.tight_layout()

xA = np.linspace(7110.5, 7113, 1000)
xB = np.linspace(7112.5, 7115, 1000)

ax = plt.subplot2grid((20,1), (4,0), colspan = 1, rowspan = 16)
plt.plot(xA, lorwslope(xA,ParamsA[0],ParamsA[1],ParamsA[2],ParamsA[3],ParamsA[4]), label = 'A peak fit, ' + str(round(ParamsA[1],1)), linewidth = 5, color = pluscolor2,zorder=1)
plt.plot(xB, lorwslope(xB,ParamsB[0],ParamsB[1],ParamsB[2],ParamsB[3],ParamsB[4]), label = 'B peak fit, ' + str(round(ParamsB[1],1)), linewidth = 5, color = minuscolor,zorder=2)
plt.errorbar(np.delete(xasProData_one.EnergyPlot,-4), np.delete(XASDiffBootF,-4), np.delete(XASDiffBootE,-4), \
             marker='.', label = str(MinTime) + ' to ' + str(MaxTime) + ' fs delay', color = 'k',zorder=10)
plt.xlabel('x-ray energy (eV)')
plt.ylabel('$I_{on}-I_{off}$')
plt.ylim([-300,150])
plt.legend()
plt.tight_layout()

axins = inset_axes(ax, width=.8, height=1.5, bbox_to_anchor=(.43, .45), bbox_transform=ax.transAxes)
axins.plot(AB, holedensity, 'o', color = '#009E73', marker = 's', label = 'calculation')
axins.plot(AB, linefit(AB), color = 'k')
axins.set_xlim([0,3])
axins.set_ylim([0,0.9])
patch = pat.Ellipse((BmA,linefit(BmA)), 2*uncertainty[1]*3/.9, 2*uncertainty[1], color='#c70039')
axins.add_patch(patch)














