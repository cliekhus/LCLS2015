# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 16:28:53 2019

@author: chelsea
"""

from numpy import loadtxt
import os
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

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


plt.figure()
plt.plot(calc00[:,0]+Eoff, calc00[:,1], label='0.00', color='k')
peaks00, A = find_peaks(calc00[:,1], height = 1e-7)
plt.plot(calc00[peaks00,0]+Eoff, calc00[peaks00,1], 'o', color='k')

plt.plot(calc40[:,0]+Eoff, calc40[:,1], label='0.40', color='b')
peaks40, A = find_peaks(calc40[:,1], height = 1e-7)
plt.plot(calc40[peaks40,0]+Eoff, calc40[peaks40,1], 'o', color='b')

plt.plot(calc55[:,0]+Eoff, calc55[:,1], label='0.55', color='g')
peaks55, A = find_peaks(calc55[:,1], height = 1e-7)
plt.plot(calc55[peaks55,0]+Eoff, calc55[peaks55,1], 'o', color='g')

plt.plot(calc72[:,0]+Eoff, calc72[:,1], label='0.72', color='y')
peaks72, A = find_peaks(calc72[:,1], height = 1e-7)
plt.plot(calc72[peaks72,0]+Eoff, calc72[peaks72,1], 'o', color='y')

plt.plot(calc77[:,0]+Eoff, calc77[:,1], label='0.77', color='r')
peaks77, A = find_peaks(calc77[:,1], height = 1e-7)
plt.plot(calc77[peaks77,0]+Eoff, calc77[peaks77,1], 'o', color='r')

plt.plot(calc86[:,0]+Eoff, calc86[:,1], label='0.86', color='m')
peaks86, A = find_peaks(calc86[:,1], height = 1e-7)
plt.plot(calc86[peaks86,0]+Eoff, calc86[peaks86,1], 'o', color='m')

plt.plot(calc100[:,0]+Eoff, calc100[:,1], label='1.00', color='c')
peaks100, A = find_peaks(calc100[:,1], height = 1e-7)
plt.plot(calc100[peaks100,0]+Eoff, calc100[peaks100,1], 'o', color='c')

plt.legend()

Apeak00 = np.min(roots00[:,0])
Apeak40 = np.min(roots40[:,0])
Apeak55 = np.min(roots55[:,0])
Apeak72 = np.min(roots72[:,0])
Apeak77 = np.min(roots77[:,0])
Apeak86 = np.min(roots86[:,0])
Apeak100 = np.min(roots100[:,0])


plt.figure(figsize = (4,5))
plt.plot([calc40[peaks40[0],0]-Apeak40,calc55[peaks55[0],0]-Apeak55,calc72[peaks72[0],0]\
          -Apeak72,calc77[peaks77[0],0]-Apeak77,calc86[peaks86[0],0]-Apeak86,calc100[peaks100[0],0]-Apeak100]\
            ,[.4,.55,.72,.77,.86,1], 'o')
plt.xlabel('A - B peak energy difference')
plt.ylabel('Fe hole density')
plt.ylim([0,1.2])
plt.xlim([0,3.5])
plt.tight_layout()

plt.figure(figsize = (4,5))
plt.plot([calc40[peaks40[0],0]-Apeak40,calc77[peaks77[0],0]-Apeak77,calc86[peaks86[0],0]-Apeak86,calc100[peaks100[0],0]-Apeak100]\
            ,[.4,.77,.86,1], 'o', linestyle='solid', label = 'calculated')
plt.plot([Params[5]-Params[2]], [0.83], linestyle='none', color='r', marker = 's', label = 'measured')
plt.xlabel('A - B peak energy difference')
plt.ylabel('Fe hole density')
plt.ylim([0,1.2])
plt.xlim([0,3.5])
plt.legend()
plt.tight_layout()





