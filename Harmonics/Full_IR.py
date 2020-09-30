# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 10:43:40 2020

@author: chelsea
"""

import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt

length=0.0050
conc=0.04

pluscolor = '#009E73'
minuscolor = '#0072b2'
pluscolor2 = '#e69f00'
red = '#c70039'

IR = loadmat('ydata.mat')
IR = IR['ydata']
IR_x = loadmat('xdata.mat')
IR_x = IR_x['xdata']

roots = loadmat('FeRu20s_IR_roots.mat')
roots = roots['FeRu20s_IR_roots']
broadened = loadmat('FeRu20s_IR.mat')
broadened = broadened['FeRu20s_IR']


plt.figure(figsize=(7.5,3))
ax=plt.subplot(1,2,1)
plt.plot(IR_x, IR/(conc*length), color = 'k')
plt.xlim([1950, 2150])
plt.xlabel('frequency (cm$^{-1}$)')
plt.ylabel('epsilon (M$^{-1}$ cm${^-1}$)')

ax=plt.subplot(1,2,2)
plt.plot(broadened[:,0], broadened[:,1], color = 'k')
markerline, stemlines, baseline = plt.stem(roots[:,0], roots[:,1]*.1, markerfmt = 'o', basefmt='none', linefmt=red)
plt.setp(markerline, 'color', red)
markerline.set_markerfacecolor('none')
markerline.set_linewidth(0.5)
markerline.set_markersize(4)
plt.setp(markerline, 'color', red)
plt.xlim([1950+130, 2150+130])
plt.xlabel('frequency (cm$^{-1}$)')
plt.ylabel('intensity (a.u.)')
plt.tight_layout()