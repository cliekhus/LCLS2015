# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 14:41:21 2020

@author: chels
"""
import numpy as np
import matplotlib.pyplot as plt
import math
from VectorFile import VectorFile

folder = "C:/Users/chelsea/OneDrive/Documents/UW/Mixed-Valence-Complexes/LCLS2015/Harmonics/FeRu-freq-xyzs/"

f = open(folder+'run.out', 'r')

contents = f.read()

data = contents.split(' ----------------------------------------------------------------------------')
infras = data[9].split('------ ---------- || -------------- ----------------- ---------- -----------\n')
infras = infras[1].split()

numinfra = int(len(infras)/7)

startindex = 6

numbers = np.empty(numinfra-startindex)
wavenumbers = np.empty(numinfra-startindex)
intensities = np.empty(numinfra-startindex)

for ii in range(startindex,numinfra):
    numbers[ii-startindex] = infras[ii*7]
    wavenumbers[ii-startindex] = infras[ii*7+1]
    intensities[ii-startindex] = infras[ii*7+3]


wn = np.linspace(0, 3500, 10000)
amp = np.zeros(np.shape(wn))
sigma = 10
scalefactor = 25

for wavenumber,intensity in zip(wavenumbers,intensities):

    amp += scalefactor*intensity/sigma/math.sqrt(2*math.pi)*np.exp(-((wn-wavenumber)/sigma)**2/2)


plt.figure(figsize=(7.5,4))
ax = plt.subplot(111)
ax.stem(wavenumbers, intensities, markerfmt = 'none', basefmt='none', linefmt='b')
ax.plot(wn, amp, 'k')
ax.set_xlim([0,400])
#ax.set_xlim([2000,2350])
ax.set_ylim([0,.08])


maxfreq = 400

#maxfreq = 2350

intensities = intensities[wavenumbers <= maxfreq]
wavenumbers = wavenumbers[wavenumbers <= maxfreq]

index = np.argsort(intensities)
index = np.flip(index)

numlines = 10
#numlines = 1

for ii in range(numlines):
    ax.annotate('', xy=(wavenumbers[index[ii]],intensities[index[ii]]+0.005), \
                xytext=(wavenumbers[index[ii]], intensities[index[ii]]+0.015), ha='center', \
                arrowprops={'arrowstyle': '->', 'ls': 'solid', 'ec': 'r', 'lw': 2})
    
ax.set_xlabel('wavenumber cm$^{-1}$')
ax.set_ylabel('IR intensity')
plt.tight_layout()

intensities = intensities[index]
wavenumbers = wavenumbers[index]
numbers = numbers[index]


intensities = intensities[:numlines]
wavenumbers = wavenumbers[:numlines]
numbers = numbers[:numlines]


index = np.argsort(wavenumbers)

file = open("distances.txt","w") 

for ii in range(numlines):
    
    file.write(str(wavenumbers[index[ii]]) + " \n")
    file.write(str(numbers[index[ii]]) + " \n")
    VectorFile(numbers[index[ii]], wavenumbers[index[ii]], False, "harmonic" + str(ii) + ".png", ii == 0, file)

file.close()

















