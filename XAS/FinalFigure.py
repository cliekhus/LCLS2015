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
    
    Cpeak1 = Croots[1]+Eoff
    Cpeak2 = Croots[3]+Eoff
    Cpeak3 = Croots[5]+Eoff

    
    return Apeak, Bpeak, Cpeak1, Cpeak2, Cpeak3





######################## GET PEAKS ##########################################
Apeaks = []
Bpeaks = []
Cpeaks1 = []
Cpeaks20 = []
Cpeaks30 = []

for ii in range(len(holedensity)):
    
    calc = loadtxt(file+'2-'+str(int(holedensity[ii]*100))+'.dat')
    roots = loadtxt(file+'2-'+str(int(holedensity[ii]*100))+'.roots')

    Apeak, Bpeak, Cpeak1, Cpeak2, Cpeak3 = makeABpeak(Eoff, calc, roots, ii%3==0, colorchoice[ii], str(holedensity[ii]), linestyle[ii])
    
    Apeaks += [Apeak]
    Bpeaks += [Bpeak]
    Cpeaks1 += [Cpeak1]
    Cpeaks20 += [Cpeak2]
    Cpeaks30 += [Cpeak3]
    

Cpeaks2 = Cpeaks30[0:2]+Cpeaks20[2:]
Cpeaks3 = Cpeaks20[0:2]+Cpeaks30[2:]

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


roots = loadtxt(file+'2-10.roots')
roots[:,0] = roots[:,0] + Eoff

Amp0 = np.zeros(np.shape(XX))
for ii in range(len(roots[:,1])):
    Amp0 = Amp0 + roots[ii,1]/np.max(roots[:,1])/((XX-roots[ii,0])**2+(.5*width)**2)/math.pi/2*width

choice = 0.68
roots = loadtxt(file+'3-'+str(choice)+'.roots')
roots[:,0] = roots[:,0] + Eoff

Amp = np.zeros(np.shape(XX))
for ii in range(len(roots[:,1])):
    Amp = Amp + roots[ii,1]/np.max(roots[:,1])/((XX-roots[ii,0])**2+(.5*width)**2)/math.pi/2*width





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
plt.stem(roots[:,0]+shift, roots[:,1]/np.max(roots[:,1]), markerfmt = 'none', basefmt='none', linefmt='k') 
plt.plot(XX+shift, Amp, color = red)
         
         


x1pos = 7113.75
x2pos = 7116.25
bally = 3.4
         
plt.plot([x1pos,x2pos], [bally,bally], lw=2, color='k')

plt.plot(x1pos,bally,'ko', markersize = 30, fillstyle = 'full', color = str(choice))
plt.plot(x2pos,bally,'ko', markersize = 30, fillstyle = 'full', color = str(1-choice))

ax.annotate('A', xy=(roots[0,0]+shift,roots[0,1]/np.max(roots[:,1])+.1), xytext=(roots[0,0]+shift,2.1), \
            ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
ax.annotate('B', xy=(roots[4,0]+shift,roots[4,1]/np.max(roots[:,1])+.1), xytext=(roots[4,0]+shift,2.1), \
            ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})

ax.text(x1pos,bally, 'Fe', horizontalalignment='center', verticalalignment='center', color='k')
ax.text(x2pos,bally, 'Ru', horizontalalignment='center', verticalalignment='center', color='w')
ax.text(x1pos,2.65, str(round(choice,2))+' hd', horizontalalignment='center', verticalalignment='center', color='k')
ax.text(x2pos,2.65, str(round(1-choice,2))+' hd', horizontalalignment='center', verticalalignment='center', color='k')


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

AB = [x-y for x,y in zip(Bpeaks, Apeaks)]
plt.plot(AB2[:,1], AB2[:,0], color = red, marker = 'o', linestyle = 'none', markerfacecolor = 'none', markeredgewidth = 1.5, label = 'traj. 1', zorder = 400)
plt.plot(AB, holedensity, color = darkred, marker = 's', linestyle = 'none', markerfacecolor = 'none', markeredgewidth = 1.5, label = 'traj. 2', zorder = 300)
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
choice = .6
roots = loadtxt(file+'2-'+str(round(choice*100))+'.roots')
roots[:,0] = roots[:,0] + Eoff

Amp0 = np.zeros(np.shape(XX))
for ii in range(len(roots[:,1])):
    Amp0 = Amp0 + roots[ii,1]/np.max(roots[:,1])/((XX-roots[ii,0])**2+(.5*width)**2)/math.pi/2*width

Fit,Params,ParamsA,ParamsB,Paramsc,cova,covb,covc = \
        fitXASPiecewiseGauss(np.delete(xasProData_one.EnergyPlot,-4), np.delete(XASDiffBootF,-4), np.delete(xasProData_one.XASOff_Norm,-4), np.delete(xasProData_one.XASOn_Norm,-4), False)

plt.figure(figsize=(3.5,5))
ax=plt.subplot(2,1,1)
plt.stem(roots[:,0]+shift, roots[:,1]/np.max(roots[:,1]), markerfmt = 'none', basefmt='none', linefmt='k') 
plt.plot(XX+shift, Amp, color = red)
         
         


x1pos = 7113.75
x2pos = 7116.25
bally = 3.4
         
plt.plot([x1pos,x2pos], [bally,bally], lw=2, color='k')

plt.plot(x1pos,bally,'ko', markersize = 30, fillstyle = 'full', color = str(choice))
plt.plot(x2pos,bally,'ko', markersize = 30, fillstyle = 'full', color = str(1-choice))

ax.annotate(' ', xy=(roots[6,0]+shift,roots[6,1]/np.max(roots[:,1])+.1), xytext=(roots[6,0]+shift,1.5), \
            ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
ax.text(roots[6,0]+shift,1.5, 'C1', horizontalalignment='right')
ax.annotate('C2', xy=(roots[8,0]+shift,roots[8,1]/np.max(roots[:,1])+.1), xytext=(roots[8,0]+shift,1.8), \
            ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
ax.annotate(' ', xy=(roots[10,0]+shift,roots[10,1]/np.max(roots[:,1])+.1), xytext=(roots[10,0]+shift,1.5), \
            ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
ax.text(roots[10,0]+shift,1.5, 'C3', horizontalalignment='left')
ax.annotate('B', xy=(roots[4,0]+shift,roots[4,1]/np.max(roots[:,1])+.1), xytext=(roots[4,0]+shift,1.8), \
            ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})

ax.text(x1pos,bally, 'Fe', horizontalalignment='center', verticalalignment='center', color='k')
ax.text(x2pos,bally, 'Ru', horizontalalignment='center', verticalalignment='center', color='w')
ax.text(x1pos,2.65, str(round(choice,2))+' hd', horizontalalignment='center', verticalalignment='center', color='k')
ax.text(x2pos,2.65, str(round(1-choice,2))+' hd', horizontalalignment='center', verticalalignment='center', color='k')


plt.xlim([7110,7120])
plt.ylim([0,4])

plt.xlabel('X-ray energy (eV)')

plt.ylabel('calculated $I_{off}$')
#ax.set_xticklabels([])

shift1 = Cpeaks1[0]-Params[5]
shift2 = Cpeaks2[0]-Params[5]
shift3 = Cpeaks3[0]-Params[5]

ax=plt.subplot(2,1,2)

BC1 = [x-y-shift1 for x,y in zip(Cpeaks1, Bpeaks)]
BC2 = [x-y-shift2 for x,y in zip(Cpeaks2, Bpeaks)]
BC3 = [x-y-shift3 for x,y in zip(Cpeaks3, Bpeaks)]

plt.plot(BC1, holedensity, color = red, marker = '^', linestyle = 'none', markerfacecolor = 'none', markeredgewidth = 1.5, label = 'C1-B', zorder = 3)
plt.plot(BC2, holedensity, color = darkred, marker = 'v', linestyle = 'none', markerfacecolor = 'none', markeredgewidth = 1.5, label = 'C2-B', zorder = 3)
plt.plot(BC3, holedensity, color = darkerred, marker = '*', linestyle = 'none', markerfacecolor = 'none', markeredgewidth = 1.5, label = 'C3-B', zorder = 3)

#choice = 0.68
#roots = loadtxt(file+'3-'+str(choice)+'.roots')
#roots[:,0] = roots[:,0] + Eoff

#Amp = np.zeros(np.shape(XX))
#for ii in range(len(roots[:,1])):
#    Amp = Amp + roots[ii,1]/np.max(roots[:,1])/((XX-roots[ii,0])**2+(.5*width)**2)/math.pi/2*width

#plt.scatter([roots[6,0]-roots[4,0]-shift1, roots[8,0]-roots[4,0]-shift2, roots[10,0]-roots[4,0]-shift3],[0.68, 0.68, 0.68])

Cline = np.polyfit(BC1+BC2+BC3, holedensity+holedensity+holedensity, 1)
Clinefit = np.poly1d(Cline)
plt.plot(BC1, Clinefit(BC1), color = 'k', zorder = 0)
patch = pat.Ellipse((FitOuts['CmB'],Clinefit(FitOuts['CmB'])), FitOuts['CmBunc'], Clinefit(FitOuts['CmB']+FitOuts['CmBunc'])-Clinefit(FitOuts['CmB']-FitOuts['CmBunc']), color=pluscolor)
#plt.plot(-10,-10, color = pluscolor, marker = 'o', label = 'exp.', linestyle = 'none')
ax.annotate('exp.', xy=(3.94,0.69), xytext=(3.54,0.83), arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
plt.tight_layout()
ax.add_patch(patch)
plt.xlabel('B - C peak energy difference (eV)')
plt.ylabel('Fe hole density')
#plt.xlim([1.5,4.5])
plt.ylim([0,1])
plt.tight_layout()



#leg = ax.legend(bbox_to_anchor=(0.8, 1.15), loc='upper left', borderaxespad=0., facecolor = 'white', handlelength = 1.2)
leg = ax.legend()
leg.get_frame().set_edgecolor('k')
leg.get_frame().set_linewidth(0.8)
leg.get_frame().set_alpha(1)





############################ Make C TDs #######################################
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

print('Hole density: ' + str(Clinefit(FitOuts['CmB'])) + ' pm ' + str(Clinefit(FitOuts['CmB']+FitOuts['CmBunc'])-Clinefit(FitOuts['CmB']-FitOuts['CmBunc'])))


print('C1 shift: ' + str(shift1))
print('C2 shift: ' + str(shift2))
print('C3 shift: ' + str(shift3))


    
print('number of points used: ' + str(FitOuts['numpoints']))











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
        ax.annotate('B', xy=(Bpeaks[ii]+shift,1.1), xytext=(Bpeaks[ii]+shift,2.1), ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
        
        ax.annotate(' ', xy=(Cpeaks1[ii]+shift,roots[6,1]/np.max(roots[:,1])+.1), xytext=(Cpeaks1[ii]+shift,2.1), \
            ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
        ax.text(Cpeaks1[ii]+shift,2.1, 'C1', horizontalalignment='right')
        ax.annotate('C2', xy=(Cpeaks2[ii]+shift,roots[8,1]/np.max(roots[:,1])+.1), xytext=(Cpeaks2[ii]+shift,2.4), \
                    ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
        ax.annotate(' ', xy=(Cpeaks3[ii]+shift,roots[10,1]/np.max(roots[:,1])+.1), xytext=(Cpeaks3[ii]+shift,2.1), \
                    ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
        ax.text(Cpeaks3[ii]+shift,2.1, 'C3', horizontalalignment='left')
        
    else:
        
        ax.text(Apeaks[ii]+shift,2.1, 'A', horizontalalignment='right')
        ax.text(Bpeaks[ii]+shift,2.1, 'B', horizontalalignment='left')
        ax.annotate('', xy=(Apeaks[ii]+shift,roots[0,1]/np.max(roots[:,1])+.1), xytext=(Apeaks[ii]+shift,2.1), ha='right', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
        ax.annotate('', xy=(Bpeaks[ii]+shift,1.1), xytext=(Bpeaks[ii]+shift,2.1), ha='left', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
        
        ax.annotate(' ', xy=(Cpeaks1[ii]+shift,roots[6,1]/np.max(roots[:,1])+.1), xytext=(Cpeaks1[ii]+shift,2.1), \
            ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
        ax.text(Cpeaks1[ii]+shift,2.1, 'C1', horizontalalignment='right')
        ax.annotate('C3', xy=(Cpeaks3[ii]+shift,roots[10,1]/np.max(roots[:,1])+.1), xytext=(Cpeaks3[ii]+shift,2.4), \
                    ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
        ax.annotate(' ', xy=(Cpeaks2[ii]+shift,roots[8,1]/np.max(roots[:,1])+.1), xytext=(Cpeaks2[ii]+shift,2.1), \
                    ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
        ax.text(Cpeaks2[ii]+shift,2.1, 'C2', horizontalalignment='left')
        
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
plt.plot(BC1, holedensity, color = red, marker = '^', linestyle = 'none', markerfacecolor = 'none', markeredgewidth = 1.5, label = 'BC 1', zorder = 3)
plt.plot(BC2, holedensity, color = darkred, marker = 'v', linestyle = 'none', markerfacecolor = 'none', markeredgewidth = 1.5, label = 'BC 2', zorder = 3)
plt.plot(BC3, holedensity, color = darkerred, marker = '*', linestyle = 'none', markerfacecolor = 'none', markeredgewidth = 1.5, label = 'BC 3', zorder = 3)
plt.plot(BC1, Clinefit(BC1), color = 'k', zorder = 0)
plt.xlabel('A - B peak energy difference (eV)')
plt.ylabel('Fe hole density')
leg = ax.legend(bbox_to_anchor=(0.03, 1.15), loc='upper left', borderaxespad=0., facecolor = 'white', handlelength = 1.2)
leg.get_frame().set_edgecolor('k')
leg.get_frame().set_linewidth(0.8)
leg.get_frame().set_alpha(1)

plt.tight_layout()