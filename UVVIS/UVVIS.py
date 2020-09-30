# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 14:10:45 2020

@author: chels
"""

import matplotlib.pyplot as plt
from numpy import loadtxt
import matplotlib.patches as pat
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
from scipy.io import loadmat

rerunTD = False

pluscolor = '#009E73'
minuscolor = '#0072b2'
pluscolor2 = '#e69f00'
red = '#c70039'

length=0.0050
conc=0.0125


"""
if rerunTD:
    import subprocess
    import time
    import os
    try:
        os.remove('UVTD.bmp')
    except:
        print('file already gone')
    subprocess.Popen('cmd /c "cd C://Program Files (x86)/University of Illinois/VMD & vmd -e C://Users/chels/OneDrive/Documents/UW/Mixed-Valence-Complexes/LCLS2015/UVVIS/UVTD.tcl"')
    time.sleep(25)
    os.system("taskkill /f /im vmd.exe")
"""
UVVIS = loadmat('FeRu125mM50um.mat')
UVVIS = UVVIS['FeRu125mM50um']

roots = np.array(loadtxt('FeRu-uvvis-200.roots'))
broadened = np.array(loadtxt('FeRu-uvvis-200.dat'))


section = UVVIS[:,0]
sectionA = UVVIS[:,1]
sectionA = sectionA[section>500]
section = section[section>500]

measmax = section[np.argmax(sectionA)]

calcmax = 1240/broadened[np.argmax(broadened[:,1]),0]

shift = 1240/measmax-1240/calcmax
print(measmax)
print(calcmax)

plt.figure(figsize=(3.3,2))

ax=plt.subplot(1,1,1)
plt.plot(UVVIS[:,0], UVVIS[:,1]/(conc*length), color = 'k')
plt.stem(1240/(roots[:,0]+shift), roots[:,1]/np.max(roots[:,1])*2000, markerfmt = 'none', basefmt='none', linefmt=red)
plt.ylabel('epsilon (M$^{-1}$cm$^{-1}$)')
plt.xlabel('wavelength (nm)')
plt.xlim([500, 2050])
plt.ylim([-50,2500])
patch = pat.Rectangle(xy=(800-25,0), width = 50, height = 2000, alpha = 0.5, color = pluscolor)
ax.add_patch(patch)
plt.tight_layout()


shift = 0


plt.figure(figsize=(7.5,3))

ax=plt.subplot(1,2,1)
plt.plot(UVVIS[:,0], UVVIS[:,1]/(conc*length), color = 'k')
plt.ylabel('epsilon (M$^{-1}$cm$^{-1}$)')
plt.xlabel('wavelength (nm)')
plt.xlim([500, 2500])
plt.ylim([-50,2500])
patch = pat.Rectangle(xy=(800-25,0), width = 50, height = 2000, alpha = 0.5, color = pluscolor)
ax.add_patch(patch)


ax=plt.subplot(1,2,2)
plt.plot(1240/broadened[1240/broadened[:,0]>0,0]+shift, broadened[1240/broadened[:,0]>0,1]/np.max(broadened[:,1]), color = 'k')
plt.stem(1240/roots[:,0]+shift, roots[:,1]/np.max(roots[:,1])*.9, markerfmt = 'none', basefmt='none', linefmt=red)

anoxpos = 1240/roots[np.argmax(roots[:,1]),0]+shift
anoypos = roots[np.argmax(roots[:,0]),1]/np.max(roots[:,1])+0.01        
"""
arr_lena = mpimg.imread('UVTD.bmp')
imagebox = OffsetImage(arr_lena, zoom=0.1)
ab = AnnotationBbox(imagebox, (2000, 0.75), frameon=False)
ax.add_artist(ab)
"""
plt.xlim([500, 2500])
plt.ylim([-0.05,1.25])
plt.ylabel('intensity (a.u.)')
plt.xlabel('wavelength (nm)')
plt.tight_layout()





plt.figure(figsize=(3.3,4))

ax=plt.subplot(2,1,1)
plt.plot(1240/UVVIS[:,0], UVVIS[:,1]/(conc*length), color = 'k')
plt.ylabel('epsilon (M$^{-1}$cm$^{-1}$)')
plt.xlabel('energy (eV)')
plt.xlim([0.3, 5])
plt.ylim([-50,2500])


ax=plt.subplot(2,1,2)
plt.plot(broadened[:,0]+shift, broadened[:,1]/np.max(broadened[:,1]), color = 'k')
markerline, stemlines, baseline = plt.stem(roots[:,0]+shift, roots[:,1]/np.max(roots[:,1])*.5, \
                                           markerfmt = 'o', basefmt='none', linefmt=red)
plt.setp(markerline, 'color', red)
markerline.set_markerfacecolor('none')
markerline.set_linewidth(0.5)
markerline.set_markersize(3)
anoxpos = 1240/roots[np.argmax(roots[:,1]),0]+shift
anoypos = roots[np.argmax(roots[:,0]),1]/np.max(roots[:,1])+0.01        
"""
arr_lena = mpimg.imread('UVTD.bmp')
imagebox = OffsetImage(arr_lena, zoom=0.1)
ab = AnnotationBbox(imagebox, (2000, 0.75), frameon=False)
ax.add_artist(ab)
"""
plt.xlim([0.3, 5])
plt.ylim([-0.05,1.25])
plt.ylabel('intensity (a.u.)')
plt.xlabel('energy (eV)')
plt.tight_layout()
