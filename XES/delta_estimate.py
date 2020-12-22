# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 16:35:17 2020

@author: chelsea
"""


import matplotlib.pyplot as plt
import h5py
import numpy as np
from scipy.optimize import curve_fit
from scipy import interpolate


def gaussian(x, a, b, c, d):
    return a*np.exp(-np.power(x - b, 2)/(2*np.power(c, 2))) + d


shift = 0.03
energy = 6404.1
excitation_fraction = 0.2

APSName = h5py.File('D:\LCLS_Data\APS\APS_Aug_2015_Fesamples.mat')

indexlow = 400
indexhigh = 500

FeRu = np.array(APSName['/FeRu_XES'])
Signal = FeRu[1][indexlow:indexhigh]
Energy = FeRu[0][indexlow:indexhigh]*1000

xmin = np.min(Energy)
xmax = np.max(Energy)

pars, cov = curve_fit(f=gaussian, xdata=Energy, ydata=Signal, p0=[12000, 6405, 1, 1000])

x = np.linspace(xmin+0.1, xmax-0.1, 100)
y = gaussian(x, *pars)

#tck = interpolate.splrep(Energy, Signal, s=0)
#unshifted = interpolate.splev(x, tck, der=0)
tck = interpolate.interp1d(Energy, Signal, kind='linear')
unshifted = tck(x)

#tck = interpolate.splrep(Energy+shift, Signal, s=0)
#pshifted = interpolate.splev(x, tck, der=0)
tck = interpolate.interp1d(Energy+shift, Signal, kind='linear')
pshifted = tck(x)

#tck = interpolate.splrep(Energy-shift, Signal, s=0)
#mshifted = interpolate.splev(x, tck, der=0)
tck = interpolate.interp1d(Energy-shift, Signal, kind='linear')
mshifted = tck(x)

plt.figure()
plt.plot(Energy, Signal)
#plt.plot(x, unshifted)
plt.plot(Energy+shift, Signal)
#plt.plot(x, pshifted)
plt.plot(Energy-shift, Signal)
#plt.plot(x, mshifted)

plt.figure(figsize = (7.5,4))
plt.plot(x, (unshifted-pshifted)/unshifted*100)
plt.plot(x, (unshifted-mshifted)/unshifted*100)
plt.xlabel('energy (eV)')
plt.ylabel('percent change')

#tck = interpolate.splrep(x, (unshifted-pshifted)/unshifted*100, s=0)
#pchange = interpolate.splev(energy, tck, der=0)
tck = interpolate.interp1d(x, (unshifted-pshifted)/unshifted*100, kind = 'linear')
pchange = tck(energy)
#tck = interpolate.splrep(x, (unshifted-mshifted)/unshifted*100, s=0)
#mchange = interpolate.splev(energy, tck, der=0)
tck = interpolate.interp1d(x, (unshifted-mshifted)/unshifted*100, kind = 'linear')
mchange = tck(energy)


plt.plot(np.array(energy), pchange, marker = 'o')
plt.plot(np.array(energy), mchange, marker = 'o')
plt.tight_layout()

print((pchange-mchange)/2*excitation_fraction)