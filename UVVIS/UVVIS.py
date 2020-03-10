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

UVVIS = loadtxt('UVVIS.txt')

plt.figure(figsize=(3.3,4))

ax=plt.subplot(2,1,2)
plt.plot(UVVIS[:,0], UVVIS[:,1], color = 'k')
plt.ylabel('absorption')
plt.xlabel('wavelength (nm)')
patch = pat.Rectangle(xy=(800-25,0), width = 50, height = 0.2, alpha = 0.5, color = '#c70039')
ax.add_patch(patch)

roots = [800, 1000, 1200]
amps = [0.05, 0.12, 0.05]
ax=plt.subplot(2,1,1)
plt.plot(UVVIS[:,0], UVVIS[:,1], color = 'k')
plt.stem(roots, amps, markerfmt = 'none', basefmt='none', linefmt='#c70039')
ax.annotate('', xy=(roots[0], amps[0]+0.01), xytext=(roots[0],0.2), ha='center', arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'k', 'lw': 2})
arr_lena = mpimg.imread('0p77T.png')
imagebox = OffsetImage(arr_lena, zoom=0.45)
ab = AnnotationBbox(imagebox, (1900, 0.13), frameon=False)
ax.add_artist(ab)
plt.ylabel('calc abs')
plt.xlabel('wavelength (nm)')
plt.tight_layout()