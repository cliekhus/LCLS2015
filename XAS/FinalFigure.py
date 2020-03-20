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
import matplotlib.image as mpimg
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox

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





#folder = "D://LCLS_Data/LCLS_python_data/XAS_Spectra/"
folder = "C:/Users/chels/Downloads/LCLS_python_data/LCLS_python_data/XAS_Spectra/"
        
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
    
    
    
pluscolor = '#009E73'
minuscolor = '#0072b2'
pluscolor2 = '#e69f00'

plt.figure(figsize = (3.5,5))


ax = plt.subplot2grid((10,1), (0,0), colspan = 1, rowspan = 2)
plt.errorbar(np.delete(xasProData_one.EnergyPlot,-4), np.delete(xasProData_one.XASOff_Norm,-4), np.delete(xasProData_one.Error_Off,-4), color = 'k')
plt.text(7112.8, 1250, 'B')
plt.text(7115, 1990, 'C')
plt.ylabel('$I_{off}$')
plt.xlim([7110,7120])
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
plt.ylim([-250,175])
plt.xlim([7110,7120])







import math

width = 1
nchoice = 0
roots = loadtxt(file+str(int(holedensity[nchoice]*100))+'.roots')

XX = np.linspace(min(xasProData_one.EnergyPlot), max(xasProData_one.EnergyPlot), 1000)
Amp0 = np.zeros(np.shape(XX))
for ii in range(len(roots[:,1])):
    Amp0 = Amp0 + roots[ii,1]/np.max(roots[:,1])/((XX-roots[ii,0]-Eoff)**2+(.5*width)**2)/math.pi/2*width


nchoice = 4
roots = loadtxt(file+str(int(holedensity[nchoice]*100))+'.roots')

XX = np.linspace(min(xasProData_one.EnergyPlot), max(xasProData_one.EnergyPlot), 1000)
Amp = np.zeros(np.shape(XX))

 

for ii in range(len(roots[:,1])):
    Amp = Amp + roots[ii,1]/np.max(roots[:,1])/((XX-roots[ii,0]-Eoff)**2+(.5*width)**2)/math.pi/2*width


Ampp = Amp[XX<7112]
XXp = XX[XX<7112]
IMax = np.argmax(Ampp)
XXA = XX[IMax]

shift = FitOuts['Ax0']-XXA
#plt.plot(XX-shift, Amp0*100)


#plt.figure()
#plt.plot(XXp, Ampp)




#plt.plot(XX+shift, (Amp-Amp0)*150, color = pluscolor,  label = 'calculation', linewidth = 2)
leg = plt.legend()
leg.get_frame().set_edgecolor('k')
leg.get_frame().set_linewidth(0.8)
plt.tight_layout()



plt.figure(figsize=(3.5,5))
ax=plt.subplot(2,1,1)
plt.stem(roots[:,0]+Eoff, roots[:,1]/np.max(roots[:,1]), markerfmt = 'none', basefmt='none', linefmt='k') 
plt.plot(XX, Amp, color = '#009E73')
         
         


x1pos = 7113.75
x2pos = 7116.25
bally = 3.4
         
plt.plot([x1pos,x2pos], [bally,bally], lw=2, color='k')

plt.plot(x1pos,bally,'ko', markersize = 30, fillstyle = 'full', color = '0.7')
plt.plot(x2pos,bally,'ko', markersize = 30, fillstyle = 'full', color = '0.3')

ax.annotate('A', xy=(Apeaks[nchoice],roots[0,1]/np.max(roots[:,1])+.1), xytext=(Apeaks[nchoice],2.1), ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
ax.annotate('B', xy=(Bpeaks[nchoice],roots[3,1]/np.max(roots[:,1])+.1), xytext=(Bpeaks[nchoice],2.1), ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})

ax.text(x1pos,bally, 'Fe', horizontalalignment='center', verticalalignment='center', color='k')
ax.text(x2pos,bally, 'Ru', horizontalalignment='center', verticalalignment='center', color='w')
ax.text(x1pos,2.65, str(holedensity[nchoice])+' hd', horizontalalignment='center', verticalalignment='center', color='k')
ax.text(x2pos,2.65, str(1-holedensity[nchoice])+' hd', horizontalalignment='center', verticalalignment='center', color='k')


plt.xlim([7110,7120])
plt.ylim([0,4])

plt.xlabel('X-ray energy (eV)')

plt.ylabel('calculated $I_{off}$')
#ax.set_xticklabels([])

ax=plt.subplot(2,1,2)

arr_lena = mpimg.imread('0p77T.png')
imagebox = OffsetImage(arr_lena, zoom=0.45)
ab = AnnotationBbox(imagebox, (0.9, 0.7), frameon=False)
ax.add_artist(ab)
ax.annotate('', xy=(1.6,0.7), xytext=(1.95,0.63), arrowprops={'arrowstyle': '<-', 'ls': 'solid', 'ec': 'k', 'lw': 2})


arr_lena = mpimg.imread('0p10T.png')
imagebox = OffsetImage(arr_lena, zoom=0.45)
ab = AnnotationBbox(imagebox, (2.2, 0.25), frameon=False)
ax.add_artist(ab)
ax.annotate('', xy=(1.5, .25), xytext=(0.4,0.1), arrowprops={'arrowstyle': '<-', 'ls': 'solid', 'ec': 'k', 'lw': 2})

AB = [x-y for x,y in zip(Bpeaks, Apeaks)]
plt.plot(AB, holedensity, 'o', color = '#009E73', marker = 's', label = 'calc.')
patch = pat.Ellipse((FitOuts['BmA'],linefit(FitOuts['BmA'])), FitOuts['BmAunc'], linefit(FitOuts['BmA']+FitOuts['BmAunc'])-linefit(FitOuts['BmA']-FitOuts['BmAunc']), color='#c70039')
plt.plot(-10,-10, color = '#c70039', marker = 'o', label = 'exp.', linestyle = 'none')
plt.tight_layout()
ax.add_patch(patch)
line = np.polyfit(AB, holedensity, 1)
linefit = np.poly1d(line)
plt.plot(AB, linefit(AB), color = 'k')
plt.xlabel('A - B peak energy difference (eV)')
plt.ylabel('Fe hole density')
plt.xlim([.12,2.9])
plt.ylim([0,1])
plt.tight_layout()

leg = ax.legend(bbox_to_anchor=(0.8, 1.15), loc='upper left', borderaxespad=0., facecolor = 'white', handlelength = 1.2)
leg.get_frame().set_edgecolor('k')
leg.get_frame().set_linewidth(0.8)
leg.get_frame().set_alpha(1)










print('Hole density: ' + str(linefit(FitOuts['BmA'])) + ' pm ' + str(linefit(FitOuts['BmA']+FitOuts['BmAunc'])-linefit(FitOuts['BmA']-FitOuts['BmAunc'])))





    
print('number of points used: ' + str(FitOuts['numpoints']))



























plt.figure(figsize=(7.5,10))

for ii in range(7):
    
    roots = loadtxt(file+str(int(holedensity[ii]*100))+'.roots')
    
    ax=plt.subplot(4,2,ii+1)
    plt.stem(roots[:,0]+Eoff, roots[:,1]/np.max(roots[:,1]), markerfmt = 'none', basefmt='none', linefmt='k')
    
    XX = np.linspace(min(xasProData_one.EnergyPlot), max(xasProData_one.EnergyPlot), 1000)
    Amp = np.zeros(np.shape(XX))
    
    
    
    for jj in range(len(roots[:,1])):
        Amp = Amp + roots[jj,1]/np.max(roots[:,1])/((XX-roots[jj,0]-Eoff)**2+(.5*width)**2)/math.pi/2*width
     
    plt.plot(XX, Amp, color = '#009E73')
    
    x1pos = 7113.75
    x2pos = 7116.25
    bally = 3.4
             
    plt.plot([x1pos,x2pos], [bally,bally], lw=2, color='k')
    
    plt.plot(x1pos,bally,'ko', markersize = 30, fillstyle = 'full', color = str(holedensity[ii]))
    plt.plot(x2pos,bally,'ko', markersize = 30, fillstyle = 'full', color = str(1-holedensity[ii]))
    
    ax.annotate('A', xy=(Apeaks[ii],roots[0,1]/np.max(roots[:,1])+.1), xytext=(Apeaks[ii],2.1), ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
    ax.annotate('B', xy=(Bpeaks[ii],1.1), xytext=(Bpeaks[ii],2.1), ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
    
    if ii <= 2:
            
        ax.text(x1pos,bally, 'Fe', horizontalalignment='center', verticalalignment='center', color='w')
        ax.text(x2pos,bally, 'Ru', horizontalalignment='center', verticalalignment='center', color='k')
        ax.text(x1pos,2.65, str(round(holedensity[ii],2))+' hd', horizontalalignment='center', verticalalignment='center', color='k')
        ax.text(x2pos,2.65, str(round(1-holedensity[ii],2))+' hd', horizontalalignment='center', verticalalignment='center', color='k')
    
    else:
    
        ax.text(x1pos,bally, 'Fe', horizontalalignment='center', verticalalignment='center', color='k')
        ax.text(x2pos,bally, 'Ru', horizontalalignment='center', verticalalignment='center', color='w')
        ax.text(x1pos,2.65, str(round(holedensity[ii],2))+' hd', horizontalalignment='center', verticalalignment='center', color='k')
        ax.text(x2pos,2.65, str(round(1-holedensity[ii],2))+' hd', horizontalalignment='center', verticalalignment='center', color='k')

    
    
    plt.xlim([7110.5,7118.5])
    plt.ylim([0,4])
    
    plt.xlabel('X-ray energy (eV)')
    plt.ylabel('absorption')
    
    #plt.ylabel('calculated $I_{off}$')

ax=plt.subplot(4,2,8)

plt.plot(AB, holedensity, 'o', color = '#009E73', marker = 's', label = 'calculation')#'#0072b2'
line = np.polyfit(AB, holedensity, 1)
linefit = np.poly1d(line)
plt.plot(AB, linefit(AB), color = 'k')
plt.xlabel('A - B peak energy difference (eV)')
plt.ylabel('Fe hole density')

plt.tight_layout()