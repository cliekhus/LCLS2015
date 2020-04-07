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

rerunTD = False

MinTime = -35
MaxTime = 35

Eoff = 143.6

ploton = False

file = os.getcwd()+'\\simulation\\feru-series-2-'

holedensity = [.10, .21, .36, .50, .60, .75, .84]
colorchoice = ['k', 'c', 'g', 'r', 'm', 'y', 'b']
linestyle = ['-', '--', '--', '--', ':', ':', ':']


pluscolor = '#009E73'
minuscolor = '#0072b2'
pluscolor2 = '#e69f00'
red = '#c70039'
darkred = '#8c0028'


def makeABpeak(Eoff, calc, roots, ploton, cc, lc, ls):
    
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
    
    #Cpeak = x[np.argmax(Cshape)]
    Cpeak = np.min(Croots)+Eoff
    #Cpeak = Croots[np.argmax(Camp)]+Eoff
    #Cpeak = Croots[3]+Eoff

    
    return Apeak, Bpeak, Cpeak





######################## GET PEAKS ##########################################
Apeaks = []
Bpeaks = []
Cpeaks = []

for ii in range(len(holedensity)):
    
    calc = loadtxt(file+str(int(holedensity[ii]*100))+'.dat')
    roots = loadtxt(file+str(int(holedensity[ii]*100))+'.roots')

    Apeak, Bpeak, Cpeak = makeABpeak(Eoff, calc, roots, ii%3==0, colorchoice[ii], str(holedensity[ii]), linestyle[ii])
    
    Apeaks += [Apeak]
    Bpeaks += [Bpeak]
    Cpeaks += [Cpeak]
    

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
plt.ylabel('Fe hole density')
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
    
    
    
    
    
    
    
    

####################### MAKE AB XANES DIFF PLOT #############################
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
xC = np.linspace(7115.5, 7120, 1000)

ax = plt.subplot2grid((10,1), (2,0), colspan = 1, rowspan = 8)
plt.fill_between(xA, FitOuts['Aoff']-xA*FitOuts['Aslope'], gauswslope(xA,FitOuts['Asig'],FitOuts['Ax0'],FitOuts['Aa'],FitOuts['Aoff'],FitOuts['Aslope']), label = 'A peak fit, ' + str(round(FitOuts['Ax0'],1)) + ' eV', linewidth = 5, color = pluscolor2,zorder=1)
plt.fill_between(xB, FitOuts['Boff']-xB*FitOuts['Bslope'], gauswslope(xB,FitOuts['Bsig'],FitOuts['Bx0'],FitOuts['Ba'],FitOuts['Boff'],FitOuts['Bslope']), label = 'B peak fit, ' + str(round(FitOuts['Bx0'],1)) + ' eV', linewidth = 5, color = pluscolor,zorder=2)
plt.errorbar(np.delete(xasProData_one.EnergyPlot,-4), np.delete(XASDiffBootF,-4), np.delete(XASDiffBootE,-4), \
             marker='.', label = str(MinTime) + ' to ' + str(MaxTime) + ' fs delay', color = 'k',zorder=10)
plt.xlabel('x-ray energy (eV)')
plt.ylabel('$I_{on}-I_{off}$')
plt.ylim([-250,175])
plt.xlim([7110,7120])






import math

width = 1.5
XX = np.linspace(7105, 7125, 1000)


nchoice = 0
roots = loadtxt(file+str(int(holedensity[nchoice]*100))+'.roots')

Amp0 = np.zeros(np.shape(XX))
for ii in range(len(roots[:,1])):
    Amp0 = Amp0 + roots[ii,1]/np.max(roots[:,1])/((XX-roots[ii,0]-Eoff)**2+(.5*width)**2)/math.pi/2*width


nchoice = 4
roots = loadtxt(file+str(int(holedensity[nchoice]*100))+'.roots')

Amp = np.zeros(np.shape(XX))
for ii in range(len(roots[:,1])):
    Amp = Amp + roots[ii,1]/np.max(roots[:,1])/((XX-roots[ii,0]-Eoff)**2+(.5*width)**2)/math.pi/2*width





Ampp = Amp[XX<7111.4]
XXp = XX[XX<7111.4]
IMax = np.argmax(Ampp)
XXA = XX[IMax]

shift = FitOuts['Ax0']-XXA




plt.plot(XX+shift, (Amp-Amp0)*200, color = red, label = 'calculation', linewidth = 2, zorder = 100)
leg = plt.legend()
leg.get_frame().set_edgecolor('k')
leg.get_frame().set_linewidth(0.8)
plt.tight_layout()











####################### AB MAKE CALCULATION PLOT ############################
plt.figure(figsize=(3.5,5))
ax=plt.subplot(2,1,1)
plt.stem(roots[:,0]+Eoff+shift, roots[:,1]/np.max(roots[:,1]), markerfmt = 'none', basefmt='none', linefmt='k') 
plt.plot(XX+shift, Amp, color = red)
         
         


x1pos = 7113.75
x2pos = 7116.25
bally = 3.4
         
plt.plot([x1pos,x2pos], [bally,bally], lw=2, color='k')

plt.plot(x1pos,bally,'ko', markersize = 30, fillstyle = 'full', color = '0.7')
plt.plot(x2pos,bally,'ko', markersize = 30, fillstyle = 'full', color = '0.3')

ax.annotate('A', xy=(Apeaks[nchoice]+shift,roots[0,1]/np.max(roots[:,1])+.1), xytext=(Apeaks[nchoice]+shift,2.1), \
            ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
ax.annotate('B', xy=(Bpeaks[nchoice]+shift,roots[3,1]/np.max(roots[:,1])+.1), xytext=(Bpeaks[nchoice]+shift,2.1), \
            ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})

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





if rerunTD:
    import subprocess
    import time
    import os
    try:
        os.remove('GS.bmp')
    except:
        print('file already gone')
    subprocess.Popen('cmd /c "cd C://Program Files (x86)/University of Illinois/VMD & vmd -e C://Users/chels/OneDrive/Documents/UW/Mixed-Valence-Complexes/LCLS2015/XAS/XASGS.tcl"')
    time.sleep(25)
    os.system("taskkill /f /im vmd.exe")
    


arr_lena = mpimg.imread('GS.bmp')
imagebox = OffsetImage(arr_lena, zoom=0.1)
ab = AnnotationBbox(imagebox, (0.9, 0.76), frameon=False)
ax.add_artist(ab)
ax.annotate('', xy=(0.4,0.48), xytext=(0.19,0.18), arrowprops={'arrowstyle': '<-', 'ls': 'solid', 'ec': 'k', 'lw': 2})


arr_lena = mpimg.imread('0p10T.png')
imagebox = OffsetImage(arr_lena, zoom=0.45)
ab = AnnotationBbox(imagebox, (2.2, 0.25), frameon=False)
ax.add_artist(ab)
ax.annotate('', xy=(2.26, 0.47), xytext=(2.3,0.62), arrowprops={'arrowstyle': '<-', 'ls': 'solid', 'ec': 'k', 'lw': 2})

AB = [x-y for x,y in zip(Bpeaks, Apeaks)]
plt.plot(AB2[:,1], AB2[:,0], color = red, marker = 'o', linestyle = 'none', markerfacecolor = 'none', markeredgewidth = 1.5, label = 'traj. 1', zorder = 400)
plt.plot(AB, holedensity, color = darkred, marker = 's', linestyle = 'none', markerfacecolor = 'none', markeredgewidth = 1.5, label = 'traj. 1', zorder = 300)
plt.plot(AB, linefit(AB), color = 'k', zorder = 1)
patch = pat.Ellipse((FitOuts['BmA'],linefit(FitOuts['BmA'])), FitOuts['BmAunc'], linefit(FitOuts['BmA']+FitOuts['BmAunc'])-linefit(FitOuts['BmA']-FitOuts['BmAunc']), color=pluscolor, zorder = 200)
#plt.plot(-10,-10, color = pluscolor, marker = 'o', label = 'exp.', linestyle = 'none')
ax.annotate('exp.', xy=(2.2,0.7), xytext=(1.9,0.85), arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
plt.tight_layout()
ax.add_patch(patch)
plt.plot(AB, linefit(AB), color = 'k', zorder = 100)
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











####################### MAKE BC XANES DIFF PLOT #############################
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
xC = np.linspace(7115.5, 7120, 1000)

ax = plt.subplot2grid((10,1), (2,0), colspan = 1, rowspan = 8)
plt.fill_between(xB, FitOuts['Boff']-xB*FitOuts['Bslope'], gauswslope(xB,FitOuts['Bsig'],FitOuts['Bx0'],FitOuts['Ba'],FitOuts['Boff'],FitOuts['Bslope']), label = 'B peak fit, ' + str(round(FitOuts['Bx0'],1)) + ' eV', linewidth = 5, color = pluscolor,zorder=2)
plt.fill_between(xC, FitOuts['Coff']-xC*FitOuts['Cslope'], gauswslope(xC,FitOuts['Csig'],FitOuts['Cx0'],FitOuts['Ca'],FitOuts['Coff'],FitOuts['Cslope']), label = 'C peak fit, ' + str(round(FitOuts['Cx0'],1)) + ' eV', linewidth = 5, color = minuscolor,zorder=3)
plt.errorbar(np.delete(xasProData_one.EnergyPlot,-4), np.delete(XASDiffBootF,-4), np.delete(XASDiffBootE,-4), \
             marker='.', label = str(MinTime) + ' to ' + str(MaxTime) + ' fs delay', color = 'k',zorder=10)
plt.xlabel('x-ray energy (eV)')
plt.ylabel('$I_{on}-I_{off}$')
plt.ylim([-250,175])
plt.xlim([7110,7120])




leg = plt.legend()
leg.get_frame().set_edgecolor('k')
leg.get_frame().set_linewidth(0.8)
plt.tight_layout()











####################### BC MAKE CALCULATION PLOT ############################
plt.figure(figsize=(3.5,5))
ax=plt.subplot(2,1,1)
plt.stem(roots[:,0]+Eoff+shift, roots[:,1]/np.max(roots[:,1]), markerfmt = 'none', basefmt='none', linefmt='k') 
plt.plot(XX+shift, Amp, color = red)
         
         


x1pos = 7113.75
x2pos = 7116.25
bally = 3.4
         
plt.plot([x1pos,x2pos], [bally,bally], lw=2, color='k')

plt.plot(x1pos,bally,'ko', markersize = 30, fillstyle = 'full', color = '0.7')
plt.plot(x2pos,bally,'ko', markersize = 30, fillstyle = 'full', color = '0.3')

ax.annotate('C', xy=(Cpeaks[nchoice]+shift,roots[5,1]/np.max(roots[:,1])+.1), xytext=(Cpeaks[nchoice]+shift,2.1), \
            ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
ax.annotate('B', xy=(Bpeaks[nchoice]+shift,roots[3,1]/np.max(roots[:,1])+.1), xytext=(Bpeaks[nchoice]+shift,2.1), \
            ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})

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
#ab = AnnotationBbox(imagebox, (0.9, 0.7), frameon=False)
#ax.add_artist(ab)
#ax.annotate('', xy=(0.4,0.48), xytext=(0.19,0.18), arrowprops={'arrowstyle': '<-', 'ls': 'solid', 'ec': 'k', 'lw': 2})


arr_lena = mpimg.imread('0p10T.png')
imagebox = OffsetImage(arr_lena, zoom=0.45)
#ab = AnnotationBbox(imagebox, (2.2, 0.25), frameon=False)
#ax.add_artist(ab)
#ax.annotate('', xy=(2.26, 0.47), xytext=(2.3,0.62), arrowprops={'arrowstyle': '<-', 'ls': 'solid', 'ec': 'k', 'lw': 2})

BC = [x-y for x,y in zip(Cpeaks, Bpeaks)]
plt.plot(BC, holedensity, color = red, marker = '^', linestyle = 'none', markerfacecolor = 'none', markeredgewidth = 1.5, label = 'traj. 1', zorder = 3)
Cline = np.polyfit(BC, holedensity, 1)
Clinefit = np.poly1d(Cline)
plt.plot(BC, Clinefit(BC), color = 'k', zorder = 0)
patch = pat.Ellipse((FitOuts['CmB'],Clinefit(FitOuts['CmB'])), FitOuts['CmBunc'], Clinefit(FitOuts['CmB']+FitOuts['CmBunc'])-Clinefit(FitOuts['CmB']-FitOuts['CmBunc']), color=pluscolor)
#plt.plot(-10,-10, color = pluscolor, marker = 'o', label = 'exp.', linestyle = 'none')
ax.annotate('exp.', xy=(3.95,0.75), xytext=(3.55,0.9), arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
plt.tight_layout()
ax.add_patch(patch)
plt.xlabel('B - C peak energy difference (eV)')
plt.ylabel('Fe hole density')
plt.xlim([1.5,4.5])
plt.ylim([0,1])
plt.tight_layout()

leg = ax.legend(bbox_to_anchor=(0.8, 1.15), loc='upper left', borderaxespad=0., facecolor = 'white', handlelength = 1.2)
leg.get_frame().set_edgecolor('k')
leg.get_frame().set_linewidth(0.8)
leg.get_frame().set_alpha(1)








print('Hole density: ' + str(Clinefit(FitOuts['CmB'])) + ' pm ' + str(Clinefit(FitOuts['CmB']+FitOuts['CmBunc'])-Clinefit(FitOuts['CmB']-FitOuts['CmBunc'])))





    
print('number of points used: ' + str(FitOuts['numpoints']))











###################### Supplementary Figure #################################



plt.figure(figsize=(7.5,10))

for ii in range(7):
    
    roots = loadtxt(file+str(int(holedensity[ii]*100))+'.roots')
    
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
        ax.annotate('B', xy=(Bpeaks[ii]+shift,1.1), xytext=(Bpeaks[ii]+shift,2.1), ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
        ax.annotate('C', xy=(Cpeaks[ii]+shift,roots[5,1]/np.max(roots[:,1])+.1), xytext=(Cpeaks[ii]+shift,2.1), ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
    
    else:
        
        ax.text(Apeaks[ii]+shift,2.1, 'A', horizontalalignment='right')
        ax.text(Bpeaks[ii]+shift,2.1, 'B', horizontalalignment='left')
        ax.annotate('', xy=(Apeaks[ii]+shift,roots[0,1]/np.max(roots[:,1])+.1), xytext=(Apeaks[ii]+shift,2.1), ha='right', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
        ax.annotate('', xy=(Bpeaks[ii]+shift,1.1), xytext=(Bpeaks[ii]+shift,2.1), ha='left', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
        ax.annotate('C', xy=(Cpeaks[ii]+shift,roots[5,1]/np.max(roots[:,1])+.1), xytext=(Cpeaks[ii]+shift,2.1), ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
    
        
    if ii <= 2:
            
        ax.text(x1pos,bally, 'Fe', horizontalalignment='center', verticalalignment='center', color='w')
        ax.text(x2pos,bally, 'Ru', horizontalalignment='center', verticalalignment='center', color='k')
        ax.text(x1pos,3.25, str(round(holedensity[ii],2))+' hd', horizontalalignment='center', verticalalignment='center', color='k')
        ax.text(x2pos,3.25, str(round(1-holedensity[ii],2))+' hd', horizontalalignment='center', verticalalignment='center', color='k')
    
    else:
    
        ax.text(x1pos,bally, 'Fe', horizontalalignment='center', verticalalignment='center', color='k')
        ax.text(x2pos,bally, 'Ru', horizontalalignment='center', verticalalignment='center', color='w')
        ax.text(x1pos,3.25, str(round(holedensity[ii],2))+' hd', horizontalalignment='center', verticalalignment='center', color='k')
        ax.text(x2pos,3.25, str(round(1-holedensity[ii],2))+' hd', horizontalalignment='center', verticalalignment='center', color='k')

    
    
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
plt.plot(BC, holedensity, color = red, marker = '^', linestyle = 'none', markerfacecolor = 'none', markeredgewidth = 1.5, label = 'BC 1', zorder = 3)
plt.plot(BC, Clinefit(BC), color = 'k', zorder = 0)
plt.xlabel('A - B peak energy difference (eV)')
plt.ylabel('Fe hole density')
leg = plt.legend()
leg.get_frame().set_edgecolor('k')
leg.get_frame().set_linewidth(0.8)
leg.get_frame().set_alpha(1)

plt.tight_layout()