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

rerunTD = False

pluscolor = '#009E73'
minuscolor = '#0072b2'
pluscolor2 = '#e69f00'
red = '#c70039'

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
UVVIS = loadtxt('UVVIS.txt')

roots = np.array(loadtxt('FeRu-uvvis-200.roots'))
broadened = np.array(loadtxt('FeRu-uvvis-200.dat'))


section = UVVIS[:,0]
sectionA = UVVIS[:,1]
sectionA = sectionA[section>500]
section = section[section>500]

measmax = section[np.argmax(sectionA)]

calcmax = 1240/broadened[np.argmax(broadened[:,1]),0]

shift = measmax-calcmax


plt.figure(figsize=(3.3,2))

ax=plt.subplot(1,1,1)
plt.plot(UVVIS[:,0], UVVIS[:,1], color = 'k')
plt.stem(1240/roots[:,0]+shift, roots[:,1]/np.max(roots[:,1])*.12, markerfmt = 'none', basefmt='none', linefmt=red)
plt.ylabel('absorption')
plt.xlabel('wavelength (nm)')
plt.xlim([200, 2500])
patch = pat.Rectangle(xy=(800-25,0), width = 50, height = 0.2, alpha = 0.5, color = pluscolor)
ax.add_patch(patch)



#shift = 0

#ax=plt.subplot(2,1,1)
#plt.plot(1240/broadened[1240/broadened[:,0]>0,0]+shift, broadened[1240/broadened[:,0]>0,1]/np.max(broadened[:,1]), color = 'k')
#plt.stem(1240/roots[:,0]+shift, roots[:,1]/np.max(roots[:,1])*.9, markerfmt = 'none', basefmt='none', linefmt=red)

#anoxpos = 1240/roots[np.argmax(roots[:,1]),0]+shift
#anoypos = roots[np.argmax(roots[:,0]),1]/np.max(roots[:,1])+0.01        
#ax.annotate('', xy=(anoxpos, 1), xytext=(anoxpos,1.2), ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
#patch = pat.Rectangle(xy=(800-25,0), width = 50, height = 1, alpha = 0.5, color = pluscolor)
#ax.add_patch(patch)
"""
arr_lena = mpimg.imread('UVTD.bmp')
imagebox = OffsetImage(arr_lena, zoom=0.1)
ab = AnnotationBbox(imagebox, (2000, 0.75), frameon=False)
ax.add_artist(ab)
"""
#plt.xlim([200, 2500])
#plt.ylim([-0.05,1.25])
#plt.ylabel('calc abs')
#plt.xlabel('wavelength (nm)')
plt.tight_layout()
