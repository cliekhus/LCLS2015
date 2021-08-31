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
from fittingfunctions import gauswslope, xasoff, xason, diffxas
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.image as mpimg
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox

rerunTD = False

MinTime = -35
MaxTime = 35

Eoff = 143.6

ploton = False

file = os.getcwd()+'\\simulation\\feru-series-'

holedensity = [.10, .21, .36, .50, .60, .75, .84]
colorchoice = ['k', 'c', 'g', 'r', 'm', 'y', 'b']
linestyle = ['-', '--', '--', '--', ':', ':', ':']


pluscolor = '#009E73'
minuscolor = '#0072b2'
pluscolor2 = '#e69f00'
red = '#c70039'
darkred = '#8c0028'
darkerred = '#64001c'


def makeABpeak(Eoff, calc, roots, ploton, cc, lc, ls):
    
    #Unfortunately, it will be difficult to code the C-peak selection process, so I am hard coding it.
    #Use Cpeak_analysis.py to see how I made the root selection.
    
    #sig = .6
    sig=1.5
    Apeak = np.min(roots[:,0])+Eoff
    Aamp = roots[0,1]

    
    x = np.array(calc[:,0])+Eoff
    x = np.linspace(np.min(calc[:,0]), np.max(calc[:,0]), 10000)+Eoff
    Broots = np.array(roots[:,0])
    Bamp = np.array(roots[:,1])
    Bamp = Bamp[Broots+Eoff<7116]
    Bamp = np.delete(Bamp, [0])
    
    Broots = Broots[Broots+Eoff<7115]
    Broots = np.delete(Broots, [0])
    Bshape = np.zeros(np.shape(x))
    for root,amp in zip(Broots,Bamp):
        Bshape = Bshape + amp*np.exp(-(x-(root+Eoff))**2/sig**2)
    
    #Bpeak = Broots[np.argmax(Bamp)]+Eoff
    
    Bpeak = x[np.argmax(Bshape)]
    Bampval = np.max(Bshape)
    
    Croots = np.array(roots[:,0])
    Camp = np.array(roots[:,1])
    Camp = Camp[Croots+Eoff>=7115]
    Croots = Croots[Croots+Eoff>=7115]
    Cshape = np.zeros(np.shape(x))
    for root,amp in zip(Croots,Camp):
        Cshape = Cshape + amp*np.exp(-(x-(root+Eoff))**2/sig**2)
    
    Cpeak1 = Croots[1]+Eoff
    Cpeak2 = Croots[3]+Eoff
    Cpeak3 = Croots[5]+Eoff

    
    return Apeak, Bpeak, Cpeak1, Cpeak2, Cpeak3, Aamp, Bampval





######################## GET PEAKS ##########################################
Apeaks = []
Bpeaks = []
Cpeaks1 = []
Cpeaks20 = []
Cpeaks30 = []
ABpeakratio = []
BampVec = []

for ii in range(len(holedensity)):
    
    calc = loadtxt(file+'2-'+str(int(holedensity[ii]*100))+'.dat')
    roots = loadtxt(file+'2-'+str(int(holedensity[ii]*100))+'.roots')

    Apeak, Bpeak, Cpeak1, Cpeak2, Cpeak3, Aamp, Bamp = makeABpeak(Eoff, calc, roots, ii%3==0, colorchoice[ii], str(holedensity[ii]), linestyle[ii])
    
    Apeaks += [Apeak]
    Bpeaks += [Bpeak]
    Cpeaks1 += [Cpeak1]
    Cpeaks20 += [Cpeak2]
    Cpeaks30 += [Cpeak3]
    ABpeakratio += [Aamp/Bamp]
    BampVec += [Bamp]
    

Cpeaks2 = Cpeaks30[0:2]+Cpeaks20[2:]
Cpeaks3 = Cpeaks20[0:2]+Cpeaks30[2:]

#Cpeaks2 = Cpeaks20
#Cpeaks3 = Cpeaks30

AB2 = loadtxt(os.getcwd()+'\\simulation\\ediff-series-3.dat')



################################# MAKE HOLE DENSITY PLOT ####################
fig, ax = plt.subplots(figsize = (4,5))
AB = [x-y for x,y in zip(Bpeaks, Apeaks)]
plt.plot(AB, holedensity, color = red, marker = 's', linestyle = 'none', markerfacecolor = 'none', label = 'trajectory 1', zorder = 3)
plt.plot(AB2[:,1], AB2[:,0], color = red, marker = 'o', linestyle = 'none', markerfacecolor = 'none', label = 'trajectory 2', zorder = 4)
line = np.polyfit(AB+list(AB2[:,1]), holedensity+list(AB2[:,0]), 1)
linefit = np.poly1d(line)
plt.plot(AB, linefit(AB), color = 'k', zorder = 0)
plt.xlabel('B - A peak energy difference')
plt.ylabel('Fe hole charge')
plt.legend()
plt.tight_layout()






###################### GET DATA #############################################
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

with open(folder + "FitOuts.pkl", "rb") as f:
    FitOuts = pickle.load(f)
    
with open(folder + "APS_HERFD_II.pkl", "rb") as f:
    HERFD_II = pickle.load(f)

with open(folder + "APS_HERFD_III.pkl", "rb") as f:
    HERFD_III = pickle.load(f)

with open(folder + "APS_incident.pkl", "rb") as f:
    incident_axis = pickle.load(f)

with open(folder + "Fe_fits.pkl", "rb") as f:
    Fe_Fits = pickle.load(f)

with open(folder + "APS_FeRu.pkl", "rb") as f:
    HERFD_FeRu = pickle.load(f)


    

params_II = Fe_Fits["params_II"]
params_XAS = Fe_Fits["params_XAS"]
print('scale factor')
scale_factor = params_XAS[1]/params_II[1]
print(scale_factor)


#Fe_Fits = {"params_II": params_II, "params_III": params_III, "params_XAS": params_XAS, "params_FeRu": params_FeRu, "cov_FeRu": np.sqrt(np.diag(cov_FeRu))}

FitOuts['BmA'] = Fe_Fits['params_FeRu'][5]-Fe_Fits['params_FeRu'][2]
FitOuts['BmAunc'] = np.sqrt((Fe_Fits['cov_FeRu'][5])**2+(Fe_Fits['cov_FeRu'][2])**2)
FitOuts['CmB'] = Fe_Fits['params_FeRu'][8]-Fe_Fits['params_FeRu'][5]
FitOuts['CmBunc'] = np.sqrt((Fe_Fits['cov_FeRu'][8])**2+(Fe_Fits['cov_FeRu'][5])**2)


####################### MAKE AB XANES DIFF PLOT #############################
plt.figure(figsize = (7,5))


energy_shift = Fe_Fits['energy_shift']
energies = np.delete(xasProData_one.EnergyPlot,-4) - energy_shift

Cmax = np.max(xasProData_one.XASOff_Norm[xasProData_one.EnergyPlot < 7118.5])-np.mean(xasProData_one.XASOff_Norm[xasProData_one.EnergyPlot < 7112.8])
HERFDmax = np.max(HERFD_FeRu[incident_axis < 7118.5])

ax = plt.subplot2grid((10,2), (0,0), colspan = 1, rowspan = 2)
plt.errorbar(energies, np.delete(xasProData_one.XASOff_Norm,-4), np.delete(xasProData_one.Error_Off,-4), color = 'k', label = 'FeRu')
plt.plot(incident_axis, (HERFD_II)*scale_factor, linewidth = 2, color = pluscolor2, linestyle = ':', label = 'FeII')
plt.plot(incident_axis, (HERFD_III)*scale_factor, linewidth = 2, color = pluscolor2, linestyle = '--', label = 'FeIII')
plt.text(7111, 900, 'A')
plt.text(7113.8, 1250, 'B')
plt.text(7115.5, 1985, 'C')
plt.ylabel('(arb. units)')
plt.xlim([7110,7122])
plt.xticks(np.arange(7110, 7123, 2.0))
plt.ylim([-100,2900])
ax.set_xticklabels([])
plt.tight_layout()

xA = np.linspace(7112, 7114, 1000)
xB = np.linspace(7114, 7117.5, 1000)

xall = np.linspace(7110, 7122, 1000)

ax = plt.subplot2grid((10,2), (2,0), colspan = 1, rowspan = 8)

params_FeRu = Fe_Fits["params_FeRu"]

#plt.plot([-100, -1000], [1,1], color = 'k', label = 'FeRu GS, LCLS')
#plt.plot([-100, -1000], [1,1], linewidth = 2, color = minuscolor, linestyle = ':', label = r'Fe$^{\mathrm{II}}$(CN)$_6$ GS, APS')
#plt.plot([-100, -1000], [1,1], linewidth = 2, color = minuscolor, linestyle = '--', label = r'Fe$^{\mathrm{III}}$(CN)$_6$ GS, APS')
plt.errorbar(energies, np.delete(XASDiffBootF,-4), np.delete(XASDiffBootE,-4), \
             marker='.', label = str(MinTime) + ' to ' + str(MaxTime) + ' fs delay', color = 'k',zorder=10, linestyle = ':')

plt.xlabel('x-ray energy (eV)')
plt.ylabel('$\Delta$ HERFD-XANES (arb. units.)')
plt.ylim([-600,185])
plt.xlim([7110,7122])
plt.xticks(np.arange(7110, 7123, 2.0))






import math

width = 1.5
XX = np.linspace(7105, 7125, 1000)


roots = loadtxt(file+'2-10.roots')
roots[:,0] = roots[:,0] + Eoff

Amp0 = np.zeros(np.shape(XX))
for ii in range(len(roots[:,1])):
    Amp0 = Amp0 + roots[ii,1]/np.max(roots[:,1])/((XX-roots[ii,0])**2+(.5*width)**2)/math.pi/2*width

choice = .60
#choice = 36
roots = loadtxt(file+'2-'+str(round(choice*100))+'.roots')
roots[:,0] = roots[:,0] + Eoff

Amp = np.zeros(np.shape(XX))
for ii in range(len(roots[:,1])):
    Amp = Amp + roots[ii,1]/np.max(roots[:,1])/((XX-roots[ii,0])**2+(.5*width)**2)/math.pi/2*width





Ampp = Amp[XX<7111.4]
XXp = XX[XX<7111.4]
IMax = np.argmax(Ampp)
XXA = XX[IMax]

Bmpp = Amp0[XX<7115]
BXXp = XX[XX<7115]
IMax = np.argmax(Bmpp)
XXB = XX[IMax]

Fit,Params,ParamsA,ParamsB,Paramsc,cova,covb,covc = \
        fitXASPiecewiseGauss(energies, np.delete(XASDiffBootF,-4), np.delete(xasProData_one.XASOff_Norm,-4), np.delete(xasProData_one.XASOn_Norm,-4), False)


#shift = FitOuts['Ax0']-XXA
#shift = FitOuts['Bx0']-XXB
#shift = 0
shift = Params[2]-Bpeaks[0]


params_FeRu = Fe_Fits["params_FeRu"]


plt.plot(incident_axis, (HERFD_III-HERFD_II)*scale_factor*.25, label = 'Fe$^{\mathrm{III}}$(CN)$_6$ - Fe$^{\mathrm{II}}$(CN)$_6$', linewidth = 3, color = pluscolor2, zorder=1)

leg = plt.legend()
leg.get_frame().set_edgecolor('k')
leg.get_frame().set_linewidth(0.8)
plt.tight_layout()






ax = plt.subplot2grid((10,2), (0,1), colspan = 1, rowspan = 2)
plt.errorbar(energies, np.delete(xasProData_one.XASOff_Norm,-4), np.delete(xasProData_one.Error_Off,-4), color = 'k')
plt.plot(incident_axis, HERFD_FeRu*scale_factor, linewidth = 2, color = minuscolor, linestyle = '-.')
plt.text(7111, 900, 'A')
plt.text(7113.8, 1250, 'B')
plt.text(7115.5, 1985, 'C')
plt.ylabel('(arb. units)')
plt.xlim([7110,7122])
plt.xticks(np.arange(7110, 7123, 2.0))
plt.ylim([-100,2900])
ax.set_xticklabels([])
plt.tight_layout()

xA = np.linspace(7112, 7114, 1000)
xB = np.linspace(7114, 7117.5, 1000)

xall = np.linspace(7110, 7122, 1000)

ax = plt.subplot2grid((10,2), (2,1), colspan = 1, rowspan = 8)

params_FeRu = Fe_Fits["params_FeRu"]

#plt.plot([-100, -1000], [1,1], color = 'k', label = 'FeRu GS, LCLS')
#plt.plot([-100, -1000], [1,1], linewidth = 2, color = pluscolor, linestyle = '-.', label = 'FeRu GS, APS')
plt.plot(xall, diffxas(xall, *params_FeRu), label = 'reconstruction', linewidth = 3, color = pluscolor, zorder = -1000)
plt.plot(xall, (params_FeRu[10]*xall + params_FeRu[9]), label = 'linear background', color = red)
#plt.fill_between(xA, FitOuts['Aoff']-xA*FitOuts['Aslope'], gauswslope(xA,FitOuts['Asig'],FitOuts['Ax0'],FitOuts['Aa'],FitOuts['Aoff'],FitOuts['Aslope']), label = 'A peak: ' + str(round(FitOuts['Ax0'],1)) + ' eV', linewidth = 5, color = pluscolor2,zorder=1)
#plt.fill_between(xB, FitOuts['Boff']-xB*FitOuts['Bslope'], gauswslope(xB,FitOuts['Bsig'],FitOuts['Bx0'],FitOuts['Ba'],FitOuts['Boff'],FitOuts['Bslope']), label = 'B peak: ' + str(round(FitOuts['Bx0'],1)) + ' eV', linewidth = 5, color = pluscolor,zorder=2)
plt.errorbar(energies, np.delete(XASDiffBootF,-4), np.delete(XASDiffBootE,-4), \
             marker='.', label = str(MinTime) + ' to ' + str(MaxTime) + ' fs delay', color = 'k', linestyle = ':', zorder = 1000)
plt.xlabel('x-ray energy (eV)')
plt.ylabel('$\Delta$ HERFD-XANES (arb. units.)')
plt.ylim([-250,135])
plt.xlim([7110,7122])
leg = plt.legend()
leg.get_frame().set_edgecolor('k')
leg.get_frame().set_linewidth(0.8)
plt.xticks(np.arange(7110, 7123, 2.0))






yvals = np.delete(XASDiffBootF,-4)
print('adjusted R2')
RSS = np.sum((diffxas(energies, *params_FeRu)*Cmax/HERFDmax*.2-yvals)**2)
TSS = np.sum((yvals - np.mean(yvals))**2)
adjR2 = 1-(RSS/(len(energies)-len(params_FeRu)-1))/(TSS/(len(energies-1)))
print(adjR2)



print('approx exc frac')







####################### AB MAKE CALCULATION PLOT ############################
plt.figure(figsize=(3.5,5))
ax=plt.subplot(2,1,1)
print('shift')
print(shift)
plt.stem(roots[:,0]+shift, roots[:,1]/np.max(roots[:,1]), markerfmt = 'none', basefmt='none', linefmt='k') 
         
         

choice = .1
#choice = 36
roots = loadtxt(file+'2-'+str(round(choice*100))+'.roots')
roots[:,0] = roots[:,0] + Eoff

Amp = np.zeros(np.shape(XX))
for ii in range(len(roots[:,1])):
    Amp = Amp + roots[ii,1]/np.max(roots[:,1])/((XX-roots[ii,0])**2+(.5*width)**2)/math.pi/2*width

x1pos = 7112.5
x2pos = 7116
bally = 4

plt.plot(XX+shift, Amp, color = red, linewidth = 2)
Ampforplotting1 = Amp


choice = .6
#choice = 36
roots = loadtxt(file+'2-'+str(round(choice*100))+'.roots')
roots[:,0] = roots[:,0] + Eoff

Amp = np.zeros(np.shape(XX))
for ii in range(len(roots[:,1])):
    Amp = Amp + roots[ii,1]/np.max(roots[:,1])/((XX-roots[ii,0])**2+(.5*width)**2)/math.pi/2*width

x1pos = 7112.5
x2pos = 7116
bally = 4

plt.plot(XX+shift, Amp, color = red, linewidth = 2)
Ampforplotting = Amp







         
plt.plot([x1pos,x2pos], [bally,bally], lw=2, color='k')

plt.plot(x1pos,bally,'ko', markersize = 30, fillstyle = 'full', color = str(choice))
plt.plot(x2pos,bally,'ko', markersize = 30, fillstyle = 'full', color = str(1-choice))

ax.annotate('A', xy=(roots[0,0]+shift,roots[0,1]/np.max(roots[:,1])+.1), xytext=(roots[0,0]+shift,2.1), \
            ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
#ax.annotate('B', xy=(roots[4,0]+shift,roots[4,1]/np.max(roots[:,1])+.1), xytext=(roots[4,0]+shift,2.1), \
#            ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
ax.annotate('B', xy=(Bpeaks[4]+shift,roots[4,1]/np.max(roots[:,1])+.3), xytext=(Bpeaks[4]+shift,2.1), \
            ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})

ax.text(x1pos,bally, 'Fe', horizontalalignment='center', verticalalignment='center', color='k')
ax.text(x2pos,bally, 'Ru', horizontalalignment='center', verticalalignment='center', color='w')
ax.text(x1pos,3.1, str(round(choice,2))+' hc', horizontalalignment='center', verticalalignment='center', color='k')
ax.text(x2pos,3.1, str(round(1-choice,2))+' hc', horizontalalignment='center', verticalalignment='center', color='k')

plt.xticks(np.arange(7110, 7123, 2.0))
plt.xlim([7110,7122])
plt.ylim([0,5])

plt.xlabel('X-ray energy (eV)')

plt.ylabel('calculated XANES')
#ax.set_xticklabels([])

ax=plt.subplot(2,1,2)




"""
if rerunTD:
    import subprocess
    import time
    import os
    try:
        os.remove('pt10_1_TD.bmp')
    except:
        print('file already gone')
    subprocess.Popen('cmd /c "cd C://Program Files (x86)/University of Illinois/VMD & vmd -e C://Users/chels/OneDrive/Documents/UW/Mixed-Valence-Complexes/LCLS2015/XAS/simulation/pt10_1_TD.tcl"')
    try:
        os.remove('pt68_1_TD.bmp')
    except:
        print('file already gone')
    subprocess.Popen('cmd /c "cd C://Program Files (x86)/University of Illinois/VMD & vmd -e C://Users/chels/OneDrive/Documents/UW/Mixed-Valence-Complexes/LCLS2015/XAS/simulation/pt10_1_TD.tcl"')
    
    time.sleep(25)
    os.system("taskkill /f /im vmd.exe")
    


arr_lena = mpimg.imread('pt10_1_TD.bmp')
imagebox = OffsetImage(arr_lena, zoom=0.1)
ab = AnnotationBbox(imagebox, (0.9, 0.76), frameon=False)
ax.add_artist(ab)
ax.annotate('', xy=(0.4,0.48), xytext=(0.19,0.18), arrowprops={'arrowstyle': '<-', 'ls': 'solid', 'ec': 'k', 'lw': 2})

arr_lena = mpimg.imread('pt68_1_TD.bmp')
imagebox = OffsetImage(arr_lena, zoom=0.1)
ab = AnnotationBbox(imagebox, (2.12, 0.23), frameon=False)
ax.add_artist(ab)
ax.annotate('', xy=(2.28, 0.50), xytext=(2.3,0.64), arrowprops={'arrowstyle': '<-', 'ls': 'solid', 'ec': 'k', 'lw': 2})
"""

AB = [x-y for x,y in zip(Bpeaks, Apeaks)]
ABx = np.linspace(.05, 3.5, 100)
plt.plot(AB2[:,1], AB2[:,0], color = red, marker = 'o', linestyle = 'none', markerfacecolor = 'none', markeredgewidth = 1.5, label = 'traj. 1', zorder = 400)
plt.plot(AB, holedensity, color = darkred, marker = 's', linestyle = 'none', markerfacecolor = 'none', markeredgewidth = 1.5, label = 'traj. 2', zorder = 300)
plt.plot(AB, linefit(AB), color = 'k', zorder = 1)
patch = pat.Ellipse((FitOuts['BmA'],linefit(FitOuts['BmA'])), FitOuts['BmAunc'], linefit(FitOuts['BmA']+FitOuts['BmAunc'])-linefit(FitOuts['BmA']-FitOuts['BmAunc']), color=pluscolor, zorder = 200)
#plt.plot(-10,-10, color = pluscolor, marker = 'o', label = 'exp.', linestyle = 'none')
ax.annotate('exp.', xy=(1.6,0.65), xytext=(.75,.65), arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
#plt.tight_layout()
ax.add_patch(patch)
plt.plot(3.2, linefit(3.2), color = pluscolor2, marker = '*', markersize = 10, linestyle = 'none', zorder = 10000)
ax.annotate('Fe$^{\mathrm{III}}$(CN)$_6$', xy=(3.2,0.88), xytext=(3.45,0.5), ha='right', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
plt.plot(ABx, linefit(ABx), color = 'k', zorder = 100)
plt.xlabel('A - B peak energy difference (eV)')
plt.ylabel('Fe hole charge')
plt.xlim([0,3.5])
plt.ylim([0,1.1])
plt.tight_layout()

#leg = ax.legend(bbox_to_anchor=(0.8, 1.15), loc='upper left', borderaxespad=0., facecolor = 'white', handlelength = 1.2)
leg = ax.legend()
leg.get_frame().set_edgecolor('k')
leg.get_frame().set_linewidth(0.8)
leg.get_frame().set_alpha(1)



plt.figure()
plt.plot(holedensity, ABpeakratio, marker = 's', label = 'calculated')
plt.xlabel('hole charge')
plt.ylabel('A, B peak amplitude ratio')
plt.plot(holedensity[4], ABpeakratio[4], marker = '*', label = '0.6 h.c.', linestyle = 'none')
plt.plot(linefit(FitOuts['BmA']), params_FeRu[1]/params_FeRu[4], marker = 'o', label='experiment', linestyle = 'none')
plt.legend()




plt.figure()
plt.plot(holedensity, [x/BampVec[0] for x in BampVec], marker = 's', label = 'calculated')
plt.xlabel('hole charge')
plt.ylabel('relative B peak amplitude')
plt.plot(linefit(FitOuts['BmA']), params_FeRu[4]/params_XAS[1], marker = 'o', label='experiment', linestyle = 'none')
plt.legend()





print('BA: ' + str(FitOuts['BmA']) + ' pm ' + str(FitOuts['BmAunc']))
print('Hole density: ' + str(linefit(FitOuts['BmA'])) + ' pm ' + str(linefit(FitOuts['BmA']+FitOuts['BmAunc'])-linefit(FitOuts['BmA']-FitOuts['BmAunc'])))












####################### MAKE BC XANES DIFF PLOT #############################
#plt.figure(figsize = (3.5,5))
#
#
#ax = plt.subplot2grid((10,1), (0,0), colspan = 1, rowspan = 2)
#plt.errorbar(np.delete(xasProData_one.EnergyPlot,-4), np.delete(xasProData_one.XASOff_Norm,-4), np.delete(xasProData_one.Error_Off,-4), color = 'k')
##plt.plot(XX+shift, Amp0*1000, linewidth = 2, color = red, linestyle = ':')
##plt.plot(XX+shift, Amp*1000, linewidth = 2, color = red, linestyle = '--')
#plt.text(7111, 900, 'A')
#plt.text(7113.8, 1250, 'B')
#plt.text(7115.5, 1985, 'C')
#plt.ylabel('$I_{off}$')
#plt.xticks(np.arange(7110, 7123, 2.0))
#plt.xlim([7110,7122])
#plt.ylim([0,2500])
#ax.set_xticklabels([])
#plt.tight_layout()
#
#xB = np.linspace(7114, 7117, 1000)
#xC = np.linspace(7117, 7122, 1000)
#
#ax = plt.subplot2grid((10,1), (2,0), colspan = 1, rowspan = 8)
#plt.fill_between(xB, FitOuts['Boff']-xB*FitOuts['Bslope'], gauswslope(xB,FitOuts['Bsig'],FitOuts['Bx0'],FitOuts['Ba'],FitOuts['Boff'],FitOuts['Bslope']), label = 'B peak: ' + str(round(FitOuts['Bx0'],1)) + ' eV', linewidth = 5, color = pluscolor,zorder=2)
#plt.fill_between(xC, FitOuts['Coff']-xC*FitOuts['Cslope'], gauswslope(xC,FitOuts['Csig'],FitOuts['Cx0'],FitOuts['Ca'],FitOuts['Coff'],FitOuts['Cslope']), label = 'C peak: ' + str(round(FitOuts['Cx0'],1)) + ' eV', linewidth = 5, color = minuscolor,zorder=3)
#plt.errorbar(np.delete(xasProData_one.EnergyPlot,-4), np.delete(XASDiffBootF,-4), np.delete(XASDiffBootE,-4), \
#             marker='.', label = str(MinTime) + ' to ' + str(MaxTime) + ' fs delay', color = 'k',zorder=10, linestyle = ':')
#plt.xlabel('x-ray energy (eV)')
#plt.ylabel('$I_{on}-I_{off}$')
#plt.ylim([-250,175])
#plt.xticks(np.arange(7110, 7123, 2.0))
#plt.xlim([7110,7122])
#
#
##calc_diff = Amp-Amp0)*200
#
##plt.plot(XX+shift, (Amp-Amp0)*200, color = red, label = 'calculation', linewidth = 2, zorder = 100)
#
#leg = plt.legend(loc = 'upper left')
#leg.get_frame().set_edgecolor('k')
#leg.get_frame().set_linewidth(0.8)
#plt.tight_layout()
#
#
#
#
#
#
#
#
######################## BC MAKE CALCULATION PLOT ############################
#choice = .5
#roots = loadtxt(file+'2-'+str(round(choice*100))+'.roots')
#roots[:,0] = roots[:,0] + Eoff
#
#Amp0 = np.zeros(np.shape(XX))
#for ii in range(len(roots[:,1])):
#    Amp0 = Amp0 + roots[ii,1]/np.max(roots[:,1])/((XX-roots[ii,0])**2+(.5*width)**2)/math.pi/2*width
#
#
#plt.figure(figsize=(3.5,5))
#ax=plt.subplot(2,1,1)
#plt.stem(roots[:,0]+shift, roots[:,1]/np.max(roots[:,1]), markerfmt = 'none', basefmt='none', linefmt='k') 
#plt.plot(XX+shift, Amp, color = red)
#         
#         
#
#
#x1pos = 7112.5
#x2pos = 7116
#bally = 3.4
#         
#plt.plot([x1pos,x2pos], [bally,bally], lw=2, color='k')
#
#plt.plot(x1pos,bally,'ko', markersize = 30, fillstyle = 'full', color = str(choice))
#plt.plot(x2pos,bally,'ko', markersize = 30, fillstyle = 'full', color = str(1-choice))
#
#ax.annotate(' ', xy=(roots[6,0]+shift,roots[6,1]/np.max(roots[:,1])+.1), xytext=(roots[6,0]+shift,1.5), \
#            ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
#ax.text(roots[6,0]+shift,1.5, 'C1', horizontalalignment='right')
#ax.annotate('C2', xy=(roots[8,0]+shift,roots[8,1]/np.max(roots[:,1])+.1), xytext=(roots[8,0]+shift,1.8), \
#            ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
#ax.annotate(' ', xy=(roots[10,0]+shift,roots[10,1]/np.max(roots[:,1])+.1), xytext=(roots[10,0]+shift,.95), \
#            ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
#ax.text(roots[10,0]+shift,.95, 'C3', horizontalalignment='left')
#ax.annotate('B', xy=(roots[4,0]+shift,roots[4,1]/np.max(roots[:,1])+.1), xytext=(roots[4,0]+shift,1.8), \
#            ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
#
#ax.text(x1pos,bally, 'Fe', horizontalalignment='center', verticalalignment='center', color='k')
#ax.text(x2pos,bally, 'Ru', horizontalalignment='center', verticalalignment='center', color='w')
#ax.text(x1pos,2.65, str(round(choice,2))+' hc', horizontalalignment='center', verticalalignment='center', color='k')
#ax.text(x2pos,2.65, str(round(1-choice,2))+' hc', horizontalalignment='center', verticalalignment='center', color='k')
#
#
#plt.xticks(np.arange(7110, 7123, 2.0))
#plt.xlim([7110,7122])
#plt.ylim([0,4])
#
#plt.xlabel('X-ray energy (eV)')
#
#plt.ylabel('calculated $I_{off}$')
##ax.set_xticklabels([])
#
##shift1 = (Cpeaks1[0]-Bpeaks[0])-(Params[5]-Params[2])
##shift2 = (Cpeaks2[0]-Bpeaks[0])-(Params[5]-Params[2])
##shift3 = (Cpeaks3[0]-Bpeaks[0])-(Params[5]-Params[2])
#
#shift1 = Cpeaks1[0]-Params[5]
#shift2 = Cpeaks2[0]-Params[5]
#shift3 = Cpeaks3[0]-Params[5]
#
#print(Cpeaks1[0])
#print()
#
#ax=plt.subplot(2,1,2)
#
#BC1 = [x-y-shift1-shift for x,y in zip(Cpeaks1, Bpeaks)]
#BC2 = [x-y-shift2-shift for x,y in zip(Cpeaks2, Bpeaks)]
#BC3 = [x-y-shift3-shift for x,y in zip(Cpeaks3, Bpeaks)]
#
#plt.plot(BC1, holedensity, color = red, marker = '^', linestyle = 'none', markerfacecolor = 'none', markeredgewidth = 1.5, label = 'C1-B', zorder = 3)
#plt.plot(BC2, holedensity, color = darkred, marker = 'v', linestyle = 'none', markerfacecolor = 'none', markeredgewidth = 1.5, label = 'C2-B', zorder = 3)
#plt.plot(BC3, holedensity, color = darkerred, marker = '*', linestyle = 'none', markerfacecolor = 'none', markeredgewidth = 1.5, label = 'C3-B', zorder = 3)
#
##choice = 0.68
##roots = loadtxt(file+'3-'+str(choice)+'.roots')
##roots[:,0] = roots[:,0] + Eoff
#
##Amp = np.zeros(np.shape(XX))
##for ii in range(len(roots[:,1])):
##    Amp = Amp + roots[ii,1]/np.max(roots[:,1])/((XX-roots[ii,0])**2+(.5*width)**2)/math.pi/2*width
#
##plt.scatter([roots[6,0]-roots[4,0]-shift1, roots[8,0]-roots[4,0]-shift2, roots[10,0]-roots[4,0]-shift3],[0.68, 0.68, 0.68])
#
#Cline = np.polyfit(BC1+BC2+BC3, holedensity+holedensity+holedensity, 1)
##Cline = np.polyfit(BC2+BC3, holedensity+holedensity, 1)
#Clinefit = np.poly1d(Cline)
#plt.plot(BC1, Clinefit(BC1), color = 'k', zorder = 0)
#patch = pat.Ellipse((FitOuts['CmB'],Clinefit(FitOuts['CmB'])), FitOuts['CmBunc'], Clinefit(FitOuts['CmB']+FitOuts['CmBunc'])-Clinefit(FitOuts['CmB']-FitOuts['CmBunc']), color=pluscolor)
##plt.plot(-10,-10, color = pluscolor, marker = 'o', label = 'exp.', linestyle = 'none')
#ax.annotate('exp.', xy=(3.73,0.6), xytext=(3.58,0.8), arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
#plt.tight_layout()
#ax.add_patch(patch)
#plt.xlabel('B - C peak energy difference (eV)')
#plt.ylabel('Fe hole charge')
##plt.xlim([1.5,4.5])
#plt.ylim([0,1])
#plt.tight_layout()
#
#
#
##leg = ax.legend(bbox_to_anchor=(0.8, 1.15), loc='upper left', borderaxespad=0., facecolor = 'white', handlelength = 1.2)
#leg = ax.legend()
#leg.get_frame().set_edgecolor('k')
#leg.get_frame().set_linewidth(0.8)
#leg.get_frame().set_alpha(1)
#
#
#


############################ Make C TDs #######################################
"""
plt.figure(figsize = (7,1.5))
ax=plt.subplot(1,1,1)

zoom = 0.11

arr_lena = mpimg.imread('pt60_5_TD.bmp')
imagebox = OffsetImage(arr_lena, zoom=zoom)
ab = AnnotationBbox(imagebox, (-.75, 0))#, frameon=False)
ax.add_artist(ab)
ax.text(-.75,-.6, 'B', horizontalalignment='center')

arr_lena = mpimg.imread('pt60_7_TD.bmp')
imagebox = OffsetImage(arr_lena, zoom=zoom)
ab = AnnotationBbox(imagebox, (-.25, 0))#, frameon=False)
ax.add_artist(ab)
ax.text(-.25,-.6, 'C1', horizontalalignment='center')

arr_lena = mpimg.imread('pt60_9_TD.bmp')
imagebox = OffsetImage(arr_lena, zoom=zoom)
ab = AnnotationBbox(imagebox, (.25, 0))#), frameon=False)
ax.add_artist(ab)
ax.text(.25,-.6, 'C2', horizontalalignment='center')

arr_lena = mpimg.imread('pt60_11_TD.bmp')
imagebox = OffsetImage(arr_lena, zoom=zoom)
ab = AnnotationBbox(imagebox, (.75, 0))#), frameon=False)
ax.add_artist(ab)
ax.text(.75,-.6, 'C3', horizontalalignment='center')

plt.xlim([-.75, .8])
plt.ylim([-.5, .5])
plt.axis('off')

frame1 = plt.gca()
frame1.axes.get_xaxis().set_visible(False)
frame1.axes.get_yaxis().set_visible(False)
"""


################# Print out info ##############################################

#print('BC: ' + str(FitOuts['CmB']) + ' pm ' + str(FitOuts['CmBunc']))
#print('Hole density: ' + str(Clinefit(FitOuts['CmB'])) + ' pm ' + str(Clinefit(FitOuts['CmB']+FitOuts['CmBunc'])-Clinefit(FitOuts['CmB']-FitOuts['CmBunc'])))


#print('C1 shift: ' + str(shift1))
#print('C2 shift: ' + str(shift2))
#print('C3 shift: ' + str(shift3))


    
#print('number of points used: ' + str(FitOuts['numpoints']))











###################### Supplementary Figure #################################



plt.figure(figsize=(7.5,10))

for ii in range(7):
    
    roots = loadtxt(file+'2-'+str(int(holedensity[ii]*100))+'.roots')
    
    ax=plt.subplot(4,2,ii+1)
    plt.stem(roots[:,0]+Eoff+shift, roots[:,1]/np.max(roots[:,1]), markerfmt = 'none', basefmt='none', linefmt='k')

    Amp = np.zeros(np.shape(XX))
    
    
    
    for jj in range(len(roots[:,1])):
        Amp = Amp + roots[jj,1]/np.max(roots[:,1])/((XX-roots[jj,0]-Eoff)**2+(.5*width)**2)/math.pi/2*width
     
    plt.plot(XX+shift, Amp, color = red)
    
    x1pos = 7113
    x2pos = 7116.25
    bally = 4.5
             
    plt.plot([x1pos,x2pos], [bally,bally], lw=2, color='k')
    
    plt.plot(x1pos,bally,'ko', markersize = 30, fillstyle = 'full', color = str(holedensity[ii]))
    plt.plot(x2pos,bally,'ko', markersize = 30, fillstyle = 'full', color = str(1-holedensity[ii]))
    
    if ii >= 2:
            
        ax.annotate('A', xy=(Apeaks[ii]+shift,roots[0,1]/np.max(roots[:,1])+.1), xytext=(Apeaks[ii]+shift,2.1), ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
        ax.annotate('B', xy=(Bpeaks[ii]+shift,1.2), xytext=(Bpeaks[ii]+shift,2.1), ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
        

        
    else:
        
        ax.text(Apeaks[ii]+shift,2.1, 'A', horizontalalignment='right')
        ax.text(Bpeaks[ii]+shift,2.1, 'B', horizontalalignment='left')
        ax.annotate('', xy=(Apeaks[ii]+shift,roots[0,1]/np.max(roots[:,1])+.1), xytext=(Apeaks[ii]+shift,2.1), ha='right', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
        ax.annotate('', xy=(Bpeaks[ii]+shift,1.2), xytext=(Bpeaks[ii]+shift,2.1), ha='left', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
        

        
    if ii <= 2:
            
        ax.text(x1pos,bally, 'Fe', horizontalalignment='center', verticalalignment='center', color='w')
        ax.text(x2pos,bally, 'Ru', horizontalalignment='center', verticalalignment='center', color='k')
        ax.text(x1pos,3.25, str(round(holedensity[ii],2))+' hc', horizontalalignment='center', verticalalignment='center', color='k')
        ax.text(x2pos,3.25, str(round(1-holedensity[ii],2))+' hc', horizontalalignment='center', verticalalignment='center', color='k')
    
    else:
    
        ax.text(x1pos,bally, 'Fe', horizontalalignment='center', verticalalignment='center', color='k')
        ax.text(x2pos,bally, 'Ru', horizontalalignment='center', verticalalignment='center', color='w')
        ax.text(x1pos,3.25, str(round(holedensity[ii],2))+' hc', horizontalalignment='center', verticalalignment='center', color='k')
        ax.text(x2pos,3.25, str(round(1-holedensity[ii],2))+' hc', horizontalalignment='center', verticalalignment='center', color='k')

        
        
    
    #plt.xlim([7110.5,7118.5])
    plt.xlim([7110.5,7125])
    plt.ylim([0,6.1])
    #plt.ylim([0,4])
    
    plt.xlabel('X-ray energy (eV)')
    plt.ylabel('absorption')
    
    #plt.ylabel('calculated $I_{off}$')

ax=plt.subplot(4,2,8)

plt.plot(AB, holedensity, color = red, marker = 's', linestyle = 'none', markerfacecolor = 'none', markeredgewidth = 1.5, label = 'AB 1', zorder = 3)
plt.plot(AB2[:,1], AB2[:,0], color = darkred, marker = 'o', linestyle = 'none', markerfacecolor = 'none', markeredgewidth = 1.5, label = 'AB 2', zorder = 4)
plt.plot(AB, linefit(AB), color = 'k', zorder = 0)
plt.xlabel('A - B peak energy difference (eV)')
plt.ylabel('Fe hole charge')
leg = ax.legend(bbox_to_anchor=(0.03, 1.15), loc='upper left', borderaxespad=0., facecolor = 'white', handlelength = 1.2)
leg.get_frame().set_edgecolor('k')
leg.get_frame().set_linewidth(0.8)
leg.get_frame().set_alpha(1)

plt.tight_layout()





####################### Presentation Figure #################################
#
#
#plt.rcParams.update({'font.size': 14})
#plt.figure(figsize=(10,3.5))
#
#for ii in range(4):
#    
#    roots = loadtxt(file+'2-'+str(int(holedensity[ii*2]*100))+'.roots')
#    
#    ax=plt.subplot(1,4,ii+1)
#    (markers, stemlines, baseline) = plt.stem(roots[:,0]+Eoff+shift, roots[:,1]/np.max(roots[:,1]), markerfmt = 'ko', basefmt='none', linefmt='k')
#    plt.setp(markers, marker='o', markeredgecolor="k", markerfacecolor='none')
#
#    Amp = np.zeros(np.shape(XX))
#    
#    
#    
#    for jj in range(len(roots[:,1])):
#        Amp = Amp + roots[jj,1]/np.max(roots[:,1])/((XX-roots[jj,0]-Eoff)**2+(.5*width)**2)/math.pi/2*width
#     
#    plt.plot(XX+shift, Amp, color = red)
#    
#    x1pos = 7113
#    x2pos = 7118
#    bally = 5.3
#    cally = 4.3
#             
#    plt.plot([x1pos,x2pos], [bally,bally], lw=2, color='k')
#    
#    plt.plot(x1pos,bally,'ko', markersize = 30, fillstyle = 'full', color = str(holedensity[ii*2]))
#    plt.plot(x2pos,bally,'ko', markersize = 30, fillstyle = 'full', color = str(1-holedensity[ii*2]))
#    
#
#        
#    if ii*2 <= 2:
#            
#        ax.text(x1pos,bally, 'Fe', horizontalalignment='center', verticalalignment='center', color='w')
#        ax.text(x2pos,bally, 'Ru', horizontalalignment='center', verticalalignment='center', color='k')
#        ax.text(x1pos,cally, "{:.2f}".format(holedensity[ii*2]), horizontalalignment='center', verticalalignment='center', color='k')
#        ax.text(x2pos,cally, "{:.2f}".format(1-holedensity[ii*2]), horizontalalignment='center', verticalalignment='center', color='k')
#    
#    else:
#    
#        ax.text(x1pos,bally, 'Fe', horizontalalignment='center', verticalalignment='center', color='k')
#        ax.text(x2pos,bally, 'Ru', horizontalalignment='center', verticalalignment='center', color='w')
#        ax.text(x1pos,cally, "{:.2f}".format(holedensity[ii*2]), horizontalalignment='center', verticalalignment='center', color='k')
#        ax.text(x2pos,cally, "{:.2f}".format(1-holedensity[ii*2]), horizontalalignment='center', verticalalignment='center', color='k')
#
#        
#        
#    
#    #plt.xlim([7110.5,7118.5])
#    plt.xlim([7110.5,7125])
#    plt.ylim([0,6.1])
#    #plt.ylim([0,4])
#    
#    plt.xlabel('X-ray energy (eV)')
#    #plt.ylabel('absorption')
#    
#    #plt.ylabel('calculated $I_{off}$')
#
#
#plt.tight_layout()
#
#
#
################################## MAKE HOLE DENSITY PLOT ####################
#fig, ax = plt.subplots(figsize = (3.2,3.5))
#AB = [x-y for x,y in zip(Bpeaks, Apeaks)]
#plt.plot(AB, holedensity, color = red, marker = 's', linestyle = 'none', markerfacecolor = 'none', label = 'traj. 1', zorder = 3)
#plt.plot(AB2[:,1], AB2[:,0], color = red, marker = 'o', linestyle = 'none', markerfacecolor = 'none', label = 'traj. 2', zorder = 4)
#plt.plot(AB, linefit(AB), color = 'k', zorder = 0)
#plt.xlabel('B - A (eV)')
#plt.ylabel('Fe hole charge')
#leg = plt.legend()
#leg.get_frame().set_edgecolor('k')
#leg.get_frame().set_linewidth(0.8)
#leg.get_frame().set_alpha(1)
#plt.tight_layout()
#
#
######################## AB MAKE CALCULATION PLOT ############################
#plt.figure(figsize=(4,4.5))
#
#ax=plt.subplot(1,1,1)
#
#AB = [x-y for x,y in zip(Bpeaks, Apeaks)]
#ABx = np.linspace(.05, 3.5, 100)
#plt.plot(AB2[:,1], AB2[:,0], color = red, marker = 'o', linestyle = 'none', markerfacecolor = 'none', markeredgewidth = 1.5, label = 'traj. 1', zorder = 400)
#plt.plot(AB, holedensity, color = darkred, marker = 's', linestyle = 'none', markerfacecolor = 'none', markeredgewidth = 1.5, label = 'traj. 2', zorder = 300)
#plt.plot(AB, linefit(AB), color = 'k', zorder = 1)
#patch = pat.Ellipse((FitOuts['BmA'],linefit(FitOuts['BmA'])), FitOuts['BmAunc'], linefit(FitOuts['BmA']+FitOuts['BmAunc'])-linefit(FitOuts['BmA']-FitOuts['BmAunc']), color=pluscolor, zorder = 200)
##plt.plot(-10,-10, color = pluscolor, marker = 'o', label = 'exp.', linestyle = 'none')
##ax.annotate('exp.', xy=(2.3,0.82), xytext=(1.55,0.9), arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
##plt.tight_layout()
##ax.add_patch(patch)
#plt.plot(3.2, linefit(3.2), color = minuscolor, marker = '*', markersize = 10, linestyle = 'none', zorder = 10000)
##ax.annotate('Fe$^{\mathrm{III}}$(CN)$_6$', xy=(3.2,0.88), xytext=(3.45,0.5), ha='right', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
#plt.plot(ABx, linefit(ABx), color = 'k', zorder = 100)
#plt.xlabel('B - A (eV)')
#plt.ylabel('Fe hole charge')
#plt.xlim([0,3.5])
#plt.ylim([0,1.1])
#plt.tight_layout()
#
##leg = ax.legend(bbox_to_anchor=(0.8, 1.15), loc='upper left', borderaxespad=0., facecolor = 'white', handlelength = 1.2)
##leg = ax.legend()
##leg.get_frame().set_edgecolor('k')
##leg.get_frame().set_linewidth(0.8)
##leg.get_frame().set_alpha(1)
#
#
######################## MAKE AB XANES DIFF PLOT #############################
#plt.figure(figsize = (4.74,1.5))
#
#ax = plt.subplot(111)
#Cmax = np.max(xasProData_one.XASOff_Norm[xasProData_one.EnergyPlot < 7118.5])-np.mean(xasProData_one.XASOff_Norm[xasProData_one.EnergyPlot < 7112.8])
#HERFDmax = np.max(HERFD_FeRu[incident_axis < 7118.5])
#
#plt.plot(np.delete(xasProData_one.EnergyPlot,-4), np.delete(xasProData_one.XASOff_Norm,-4), color = 'k', label = 'FeRu')
#plt.plot(incident_axis, (HERFD_II)*Cmax/HERFDmax, linewidth = 2, color = minuscolor, linestyle = ':', label = 'FeII')
#plt.plot(incident_axis, (HERFD_III)*Cmax/HERFDmax, linewidth = 2, color = minuscolor, linestyle = '--', label = 'FeIII')
#plt.text(7111, 900, 'A')
#plt.text(7113.8, 1250, 'B')
#plt.text(7115.4, 2000, 'C')
#plt.ylabel('HERFD-XANES')
#plt.xlim([7110,7122])
#plt.xticks(np.arange(7110, 7123, 2.0))
#plt.ylim([-100,2900])
#leg = ax.legend(bbox_to_anchor=(.73, .6), loc='upper left', borderaxespad=0., facecolor = 'white', handlelength = 1.2, fontsize=12)
#leg.get_frame().set_edgecolor('k')
#leg.get_frame().set_linewidth(0.8)
#leg.get_frame().set_alpha(1)
#ax.set_xticklabels([])
#plt.tight_layout()
#
#xA = np.linspace(7112, 7114, 1000)
#xB = np.linspace(7114, 7117.5, 1000)
#
#xall = np.linspace(7110, 7122, 1000)
#
#
#plt.figure(figsize = (5, 4.5))
##ax = plt.subplot2grid((10,10), (2,1), colspan = 9, rowspan = 7)
#
#params_FeRu = Fe_Fits["params_FeRu"]
#
##plt.plot([-100, -1000], [1,1], color = 'k', label = 'FeRu GS, LCLS')
##plt.plot([-100, -1000], [1,1], linewidth = 2, color = minuscolor, linestyle = ':', label = r'Fe$^{\mathrm{II}}$(CN)$_6$ GS, APS')
##plt.plot([-100, -1000], [1,1], linewidth = 2, color = minuscolor, linestyle = '--', label = r'Fe$^{\mathrm{III}}$(CN)$_6$ GS, APS')
#plt.errorbar(np.delete(xasProData_one.EnergyPlot,-4), np.delete(XASDiffBootF,-4), np.delete(XASDiffBootE,-4), \
#             marker='.', label = str(MinTime) + ' to ' + str(MaxTime) + ' fs delay', color = 'k',zorder=10, linestyle = ':')
#
#plt.xlabel('X-ray energy (eV)')
#plt.ylabel('$\Delta$ HERFD-XANES')
#plt.ylim([-550,185])
#plt.xlim([7110,7122])
#plt.xticks(np.arange(7110, 7123, 2.0))
#
#
#
#
#
#
#import math
#
#width = 1.5
#XX = np.linspace(7105, 7125, 1000)
#
#
#roots = loadtxt(file+'2-10.roots')
#roots[:,0] = roots[:,0] + Eoff
#
#Amp0 = np.zeros(np.shape(XX))
#for ii in range(len(roots[:,1])):
#    Amp0 = Amp0 + roots[ii,1]/np.max(roots[:,1])/((XX-roots[ii,0])**2+(.5*width)**2)/math.pi/2*width
#
#choice = .75
##choice = 36
#roots = loadtxt(file+'2-'+str(round(choice*100))+'.roots')
#roots[:,0] = roots[:,0] + Eoff
#
#Amp = np.zeros(np.shape(XX))
#for ii in range(len(roots[:,1])):
#    Amp = Amp + roots[ii,1]/np.max(roots[:,1])/((XX-roots[ii,0])**2+(.5*width)**2)/math.pi/2*width
#
#
#
#
#
#Ampp = Amp[XX<7111.4]
#XXp = XX[XX<7111.4]
#IMax = np.argmax(Ampp)
#XXA = XX[IMax]
#
#Bmpp = Amp0[XX<7115]
#BXXp = XX[XX<7115]
#IMax = np.argmax(Bmpp)
#XXB = XX[IMax]
#
#Fit,Params,ParamsA,ParamsB,Paramsc,cova,covb,covc = \
#        fitXASPiecewiseGauss(np.delete(xasProData_one.EnergyPlot,-4), np.delete(XASDiffBootF,-4), np.delete(xasProData_one.XASOff_Norm,-4), np.delete(xasProData_one.XASOn_Norm,-4), False)
#
#
##shift = FitOuts['Ax0']-XXA
##shift = FitOuts['Bx0']-XXB
##shift = 0
#shift = Params[2]-Bpeaks[0]
#
#
#
#
#
#plt.plot(incident_axis, (HERFD_III-HERFD_II)*Cmax/HERFDmax*.2, label = 'Fe$^{\mathrm{III}}$(CN)$_6$ - Fe$^{\mathrm{II}}$(CN)$_6$', linewidth = 3, color = pluscolor2, zorder=1)
#
##leg = plt.legend()
##leg.get_frame().set_edgecolor('k')
##leg.get_frame().set_linewidth(0.8)
#plt.tight_layout()
#
#
#
#
#
#plt.figure(figsize = (3.5,1))
##ax = plt.subplot2grid((10,1), (0,0), colspan = 1, rowspan = 2)
#plt.errorbar(np.delete(xasProData_one.EnergyPlot,-4), np.delete(xasProData_one.XASOff_Norm,-4), np.delete(xasProData_one.Error_Off,-4), color = 'k')
#plt.plot(incident_axis, (HERFD_II)*Cmax/HERFDmax, linewidth = 2, color = minuscolor, linestyle = ':', label = 'FeII')
#plt.plot(incident_axis, (HERFD_III)*Cmax/HERFDmax, linewidth = 2, color = minuscolor, linestyle = '--', label = 'FeIII')
#plt.text(7111, 900, 'A')
#plt.text(7113.8, 1250, 'B')
#plt.text(7115.5, 1985, 'C')
##plt.ylabel('(arb. units)')
#plt.xlim([7110,7122])
#plt.xticks(np.arange(7110, 7123, 2.0))
#plt.ylim([-100,2900])
##ax.set_xticklabels([])
#plt.tight_layout()
#
#xA = np.linspace(7112, 7114, 1000)
#xB = np.linspace(7114, 7117.5, 1000)
#
#xall = np.linspace(7110, 7122, 1000)
#
##ax = plt.subplot2grid((10,1), (2,0), colspan = 1, rowspan = 7)
#
#plt.figure(figsize = (5,4.5))
#params_FeRu = Fe_Fits["params_FeRu"]
#
##plt.plot([-100, -1000], [1,1], color = 'k', label = 'FeRu GS, LCLS')
##plt.plot([-100, -1000], [1,1], linewidth = 2, color = pluscolor, linestyle = '-.', label = 'FeRu GS, APS')
#plt.plot(xall, diffxas(xall, *params_FeRu)*Cmax/HERFDmax*.2, label = 'reconstruction', linewidth = 3, color = pluscolor, zorder = -1000)
##plt.fill_between(xA, FitOuts['Aoff']-xA*FitOuts['Aslope'], gauswslope(xA,FitOuts['Asig'],FitOuts['Ax0'],FitOuts['Aa'],FitOuts['Aoff'],FitOuts['Aslope']), label = 'A peak: ' + str(round(FitOuts['Ax0'],1)) + ' eV', linewidth = 5, color = pluscolor2,zorder=1)
##plt.fill_between(xB, FitOuts['Boff']-xB*FitOuts['Bslope'], gauswslope(xB,FitOuts['Bsig'],FitOuts['Bx0'],FitOuts['Ba'],FitOuts['Boff'],FitOuts['Bslope']), label = 'B peak: ' + str(round(FitOuts['Bx0'],1)) + ' eV', linewidth = 5, color = pluscolor,zorder=2)
#plt.errorbar(np.delete(xasProData_one.EnergyPlot,-4), np.delete(XASDiffBootF,-4), np.delete(XASDiffBootE,-4), \
#             marker='.', label = str(MinTime) + ' to ' + str(MaxTime) + ' fs delay', color = 'k', linestyle = ':', zorder = 1000)
#plt.xlabel('X-ray energy (eV)')
#plt.ylabel('$\Delta$ HERFD-XANES')
#plt.ylim([-250,100])
#plt.xlim([7110,7122])
##leg = plt.legend()
##leg.get_frame().set_edgecolor('k')
##leg.get_frame().set_linewidth(0.8)
#plt.xticks(np.arange(7110, 7123, 2.0))
#plt.tight_layout()
#
#
#
#
#
#
#
#
#
#
#print('scale factor')
#print(Cmax/HERFDmax*.2)
#print(Cmax/HERFDmax)
#
#
#
#with open(r"D:\LCLS_Data\LCLS_python_data\XAS_Spectra\for_model_incident.pkl", "wb") as f:
#    pickle.dump(np.delete(xasProData_one.EnergyPlot,-4), f)
#with open(r"D:\LCLS_Data\LCLS_python_data\XAS_Spectra\for_model_GS.pkl", "wb") as f:
#    pickle.dump(np.delete(xasProData_one.XASOff_Norm,-4), f)
