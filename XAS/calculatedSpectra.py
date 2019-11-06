# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 16:28:53 2019

@author: chelsea
"""

from numpy import loadtxt
import os
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import matplotlib.patches as pat
import numpy as np

Eoff = 143.6

calc00 = loadtxt(os.getcwd()+'\\simulation\\feru-series-fe-0_00.dat')
calc40 = loadtxt(os.getcwd()+'\\simulation\\feru-series-fe-0_40.dat')
calc55 = loadtxt(os.getcwd()+'\\simulation\\feru-series-fe-0_55.dat')
calc72 = loadtxt(os.getcwd()+'\\simulation\\feru-series-fe-0_72.dat')
calc77 = loadtxt(os.getcwd()+'\\simulation\\feru-series-fe-0_77.dat')
calc86 = loadtxt(os.getcwd()+'\\simulation\\feru-series-fe-0_86.dat')
calc100 = loadtxt(os.getcwd()+'\\simulation\\feru-series-fe-1_00.dat')

roots00 = loadtxt(os.getcwd()+'\\simulation\\feru-series-fe-0_00.roots')
roots40 = loadtxt(os.getcwd()+'\\simulation\\feru-series-fe-0_40.roots')
roots55 = loadtxt(os.getcwd()+'\\simulation\\feru-series-fe-0_55.roots')
roots72 = loadtxt(os.getcwd()+'\\simulation\\feru-series-fe-0_72.roots')
roots77 = loadtxt(os.getcwd()+'\\simulation\\feru-series-fe-0_77.roots')
roots86 = loadtxt(os.getcwd()+'\\simulation\\feru-series-fe-0_86.roots')
roots100 = loadtxt(os.getcwd()+'\\simulation\\feru-series-fe-1_00.roots')


plt.legend()

Apeak00 = np.min(roots00[:,0])
Apeak40 = np.min(roots40[:,0])
Apeak55 = np.min(roots55[:,0])
Apeak72 = np.min(roots72[:,0])
Apeak77 = np.min(roots77[:,0])
Apeak86 = np.min(roots86[:,0])
Apeak100 = np.min(roots100[:,0])

sig = .5

x00 = np.array(calc00[:,0])+Eoff
Broots00 = np.array(roots00[:,0])
Bamp00 = np.array(roots00[:,1])
Bamp00 = Bamp00[Broots00+Eoff<7116]
Bamp00 = np.delete(Bamp00, [0])
Broots00 = Broots00[Broots00+Eoff<7116]
Broots00 = np.delete(Broots00, [0])
Bshape00 = np.zeros(np.shape(x00))
for root,amp in zip(Broots00,Bamp00):
    print('hi')
    Bshape00 = Bshape00 + amp/50*np.exp(-(x00-(root+Eoff))**2/sig**2)

Bpeak00 = x00[np.argmax(Bshape00)]


plt.figure()
plt.plot(calc00[:,0]+Eoff, calc00[:,1], label='0.00', color='k')
peaks00, A = find_peaks(calc00[:,1], height = 1e-7)
plt.plot(calc00[peaks00,0]+Eoff, calc00[peaks00,1], 'o', color='k')

plt.plot(x00, Bshape00, color = 'k')


plt.plot(calc40[:,0]+Eoff, calc40[:,1], label='0.40', color='b')
peaks40, A = find_peaks(calc40[:,1], height = 1e-7)
plt.plot(calc40[peaks40,0]+Eoff, calc40[peaks40,1], 'o', color='b')



x40 = np.array(calc40[:,0])+Eoff
Broots40 = np.array(roots40[:,0])
Bamp40 = np.array(roots55[:,1])
Bamp40 = Bamp40[Broots40+Eoff<7116]
Bamp40 = np.delete(Bamp40, [0])
Broots40 = Broots40[Broots40+Eoff<7116]
Broots40 = np.delete(Broots40, [0])
Bshape40 = np.zeros(np.shape(x40))
for root,amp in zip(Broots40,Bamp40):
    print('hi')
    Bshape40 = Bshape40 + amp/50*np.exp(-(x40-(root+Eoff))**2/sig**2)

Bpeak40 = x40[np.argmax(Bshape40)]
plt.plot(x40, Bshape40, color = 'b')


plt.plot(calc55[:,0]+Eoff, calc55[:,1], label='0.55', color='g')
peaks55, A = find_peaks(calc55[:,1], height = 1e-7)
plt.plot(calc55[peaks55,0]+Eoff, calc55[peaks55,1], 'o', color='g')



x55 = np.array(calc55[:,0])+Eoff
Broots55 = np.array(roots55[:,0])
Bamp55 = np.array(roots55[:,1])
Bamp55 = Bamp55[Broots55+Eoff<7116]
Bamp55 = np.delete(Bamp55, [0])
Broots55 = Broots55[Broots55+Eoff<7116]
Broots55 = np.delete(Broots55, [0])
Bshape55 = np.zeros(np.shape(x55))
for root,amp in zip(Broots55,Bamp55):
    print('hi')
    Bshape55 = Bshape55 + amp/50*np.exp(-(x55-(root+Eoff))**2/sig**2)

Bpeak55 = x55[np.argmax(Bshape55)]
plt.plot(x55, Bshape55, color = 'g')

plt.plot(calc72[:,0]+Eoff, calc72[:,1], label='0.72', color='y')
peaks72, A = find_peaks(calc72[:,1], height = 1e-7)
plt.plot(calc72[peaks72,0]+Eoff, calc72[peaks72,1], 'o', color='y')

plt.plot(calc77[:,0]+Eoff, calc77[:,1], label='0.77', color='r')
peaks77, A = find_peaks(calc77[:,1], height = 1e-7)
plt.plot(calc77[peaks77,0]+Eoff, calc77[peaks77,1], 'o', color='r')


x77 = np.array(calc77[:,0])+Eoff
Broots77 = np.array(roots77[:,0])
Bamp77 = np.array(roots77[:,1])
Bamp77 = Bamp77[Broots77+Eoff<7116]
Bamp77 = np.delete(Bamp77, [0])
Broots77 = Broots77[Broots77+Eoff<7116]
Broots77 = np.delete(Broots77, [0])
Bshape77 = np.zeros(np.shape(x77))
for root,amp in zip(Broots77,Bamp77):
    print('hi')
    Bshape77 = Bshape77 + amp/50*np.exp(-(x77-(root+Eoff))**2/sig**2)

Bpeak77 = x77[np.argmax(Bshape77)]
plt.plot(x77, Bshape77, color = 'r')



plt.plot(calc86[:,0]+Eoff, calc86[:,1], label='0.86', color='m')
peaks86, A = find_peaks(calc86[:,1], height = 1e-7)
plt.plot(calc86[peaks86,0]+Eoff, calc86[peaks86,1], 'o', color='m')



x86 = np.array(calc86[:,0])+Eoff
Broots86 = np.array(roots86[:,0])
Bamp86 = np.array(roots86[:,1])
Bamp86 = Bamp86[Broots86+Eoff<7116]
Bamp86 = np.delete(Bamp86, [0])
Broots86 = Broots86[Broots86+Eoff<7116]
Broots86 = np.delete(Broots86, [0])
Bshape86 = np.zeros(np.shape(x86))
for root,amp in zip(Broots86,Bamp86):
    print('hi')
    Bshape86 = Bshape86 + amp/50*np.exp(-(x86-(root+Eoff))**2/sig**2)

Bpeak86 = x86[np.argmax(Bshape86)]
plt.plot(x86, Bshape86, color = 'm')


plt.plot(calc100[:,0]+Eoff, calc100[:,1], label='1.00', color='c')
peaks100, A = find_peaks(calc100[:,1], height = 1e-7)
plt.plot(calc100[peaks100,0]+Eoff, calc100[peaks100,1], 'o', color='c')



x100 = np.array(calc100[:,0])+Eoff
Broots100 = np.array(roots100[:,0])
Bamp100 = np.array(roots100[:,1])
Bamp100 = Bamp100[Broots100+Eoff<7116]
Bamp100 = np.delete(Bamp100,[0])
Broots100 = Broots100[Broots100+Eoff<7116]
Broots100 = np.delete(Broots100,[0])
Bshape100 = np.zeros(np.shape(x100))
for root,amp in zip(Broots100,Bamp100):
    print('hi')
    Bshape100 = Bshape100 + amp/50*np.exp(-(x100-(root+Eoff))**2/sig**2)

Bpeak100 = x100[np.argmax(Bshape100)]
plt.plot(x100, Bshape100, color = 'c')


plt.figure(figsize = (4,5))
plt.plot([calc40[peaks40[0],0]-Apeak40,calc55[peaks55[0],0]-Apeak55,calc72[peaks72[0],0]\
          -Apeak72,calc77[peaks77[0],0]-Apeak77,calc86[peaks86[0],0]-Apeak86,calc100[peaks100[0],0]-Apeak100]\
            ,[.4,55,.72,.77,.86,1], 'o')
plt.xlabel('A - B peak energy difference')
plt.ylabel('Fe hole density')
plt.ylim([0,1.2])
plt.xlim([0,3.5])
plt.tight_layout()

fig, ax = plt.subplots(figsize = (4,5))
patch = pat.Ellipse((ParamsDiff[5]-ParamsDiff[2],.826), 0.2, 0.03, color='r')
ax.add_patch(patch)
plt.plot([Bpeak40-Apeak40-Eoff,Bpeak77-Apeak77-Eoff,Bpeak86-Apeak86-Eoff,Bpeak100-Apeak100-Eoff]\
            ,[.4,.77,.86,1], 'o', linestyle='solid', label = 'calculated')
plt.xlabel('A - B peak energy difference')
plt.ylabel('Fe hole density')
plt.ylim([0,1.2])
plt.xlim([0,3.5])
plt.legend()
plt.tight_layout()





