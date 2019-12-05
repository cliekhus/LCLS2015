# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 15:46:10 2019

@author: chelsea
"""

import matplotlib.pyplot as plt
import numpy as np
import math

V = np.array([2144.551,2158.833,2182.388,2195.579,2207.034,2239.239])
A = np.array([11.291,13.279,6.533,5.761,12.454,1.156])


x = np.linspace(2000, 2500,100000)
S = 0*x
for v,a in zip(V,A):

    S = S+a*np.exp(-(x-v)**2/100)
    
Sp = S[np.logical_and(x>2180, x<2216)]
index = np.argmax(Sp)
xp = x[np.logical_and(x>2180, x<2216)]

print(xp[index])

plt.figure()
plt.plot(x,S)
plt.stem(V,A)