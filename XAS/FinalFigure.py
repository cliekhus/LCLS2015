# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 16:28:53 2019
@author: chelsea
"""

from numpy import loadtxt
import os
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import numpy as np
import pickle
import matplotlib.gridspec as gridspec
from fitXASDiff import fitXASPiecewiseGauss
from fittingfunctions import gauswslope
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
    
    x = np.array(calc[:,0])+Eoff
    Broots = np.array(roots[:,0])
    Bamp = np.array(roots[:,1])
    Bamp = Bamp[Broots+Eoff<7114]
    Bamp = np.delete(Bamp, [0])
    
    Broots = Broots[Broots+Eoff<7114]
    Broots = np.delete(Broots, [0])
    Bshape = np.zeros(np.shape(x))
    for root,amp in zip(Broots,Bamp):
        Bshape = Bshape + amp*np.exp(-(x-(root+Eoff))**2/sig**2)
    
    Bpeak = Broots[np.argmax(Bamp)]+Eoff

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
    
    Apeaks += [Apeak]
    Bpeaks += [Bpeak]
    





fig, ax = plt.subplots(figsize = (4,5))
AB = [x-y for x,y in zip(Bpeaks, Apeaks)]
plt.plot(AB, holedensity, 'o', color = '#009E73', marker = 's', label = 'calculation')#'#0072b2'
line = np.polyfit(AB, holedensity, 1)
linefit = np.poly1d(line)
plt.plot(AB, linefit(AB), color = 'k')
plt.xlabel('B - A peak energy difference')
plt.ylabel('Fe hole density')
plt.tight_layout()






with open("D://LCLS_Data/LCLS_python_data/XAS_Spectra/FitOuts.pkl", "rb") as f:
    FitOuts = pickle.load(f)

patch = pat.Ellipse((FitOuts['BmA'],linefit(FitOuts['BmA'])), FitOuts['BmAunc'], linefit(FitOuts['BmAunc']), color='#c70039')
ax.add_patch(patch)
plt.ylim([0,1])
plt.xlim([0,3])
plt.plot([-1,-2], [1,2], marker = 'o', label = 'measurement', color = '#c70039', linestyle = 'none')#'#e69f00'
leg = plt.legend()
leg.get_frame().set_edgecolor('k')


print('Hole density: ' + str(linefit(FitOuts['BmA'])) + ' pm ' + str(linefit(FitOuts['BmAunc'])))


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



    

pluscolor = '#009E73'
minuscolor = '#0072b2'
pluscolor2 = '#e69f00'

plt.figure(figsize = (4,5))

gridspec.GridSpec(10,1)

ax = plt.subplot2grid((10,1), (0,0), colspan = 1, rowspan = 2)
plt.errorbar(np.delete(xasProData_one.EnergyPlot,-4), np.delete(xasProData_one.XASOff_Norm,-4), np.delete(xasProData_one.Error_Off,-4), color = 'k')
plt.text(7112.8, 1250, 'B')
plt.text(7115, 1990, 'C')
plt.ylabel('$I_{off}$')
ax.set_xticklabels([])
plt.tight_layout()

xA = np.linspace(7110.5, 7113, 1000)
xB = np.linspace(7112.5, 7115, 1000)

ax = plt.subplot2grid((10,1), (2,0), colspan = 1, rowspan = 8)
plt.fill_between(xA, FitOuts['Aoff']-xA*FitOuts['Aslope'], gauswslope(xA,FitOuts['Asig'],FitOuts['Ax0'],FitOuts['Aa'],FitOuts['Aoff'],FitOuts['Aslope']), label = 'A peak fit, ' + str(round(FitOuts['Ax0'],1)) + ' eV', linewidth = 5, color = pluscolor2,zorder=1)
plt.fill_between(xB, FitOuts['Boff']-xB*FitOuts['Bslope'], gauswslope(xB,FitOuts['Bsig'],FitOuts['Bx0'],FitOuts['Ba'],FitOuts['Boff'],FitOuts['Bslope']), label = 'B peak fit, ' + str(round(FitOuts['Bx0'],1)) + ' eV', linewidth = 5, color = minuscolor,zorder=2)
plt.errorbar(np.delete(xasProData_one.EnergyPlot,-4), np.delete(XASDiffBootF,-4), np.delete(XASDiffBootE,-4), \
             marker='.', label = str(MinTime) + ' to ' + str(MaxTime) + ' fs delay', color = 'k',zorder=10)
plt.xlabel('x-ray energy (eV)')
plt.ylabel('$I_{on}-I_{off}$')
plt.ylim([-250,150])
leg = plt.legend()
leg.get_frame().set_edgecolor('k')
leg.get_frame().set_linewidth(0.8)
plt.tight_layout()


print('number of points used: ' + str(FitOuts['numpoints']))

"""
axins = inset_axes(ax, width=.8, height=1.5, bbox_to_anchor=(.43, .45), bbox_transform=ax.transAxes)
axins.plot(AB, holedensity, 'o', color = '#009E73', marker = 's', label = 'calculation')
axins.plot(AB, linefit(AB), color = 'k')
axins.set_xlim([0,3])
axins.set_ylim([0,0.9])
#patch = pat.Ellipse((BmA,linefit(BmA)), 5*uncertainty[1], linefit(BmA+uncertainty[1]*5)-linefit(BmA-uncertainty[1]*5), color='#c70039')
patch = pat.Ellipse((BmA,linefit(BmA)), 1.9, linefit(1.8+1.9)-linefit(1.8-1.9), color='#c70039')
axins.add_patch(patch)
"""












