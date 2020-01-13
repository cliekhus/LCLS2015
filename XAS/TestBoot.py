# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 13:19:56 2020

@author: chelsea
"""

import numpy as np

#Rainbow = ["5EBD3D", "FFB900", "F78200", "E23838", "973999", "009CDF"]
Rainbow = ["FF0000", "FF7F00", "FFFF00", "00FF00", "0000FF", "4B0082", "9400D3"]
Rainbow = reversed(Rainbow)
index = np.linspace(0,1,7)
RainbowInt = [int(bow,16) for bow in Rainbow]

RainInt = np.interp(np.linspace(0,1,np.shape(XASDiffBoot)[1]), index, RainbowInt)

RainHex = ["#"+hex(int(bow)).replace('0x','').zfill(6) for bow in RainInt]           

plt.figure()
#for ii in range(len(RainHex)):
for ii in range(100):
    #plt.plot(np.delete(xasProData_one.EnergyPlot,-4), np.delete(XASDiffBoot[:,ii],-4), color = RainHex[ii], alpha = 0.3, label = str(ii))
    #plt.plot(np.delete(xasProData_one.EnergyPlot,-4), np.delete(XASDiffBoot[:,ii],-4), color = 'k', alpha = 0.2, label = str(ii))
    plt.plot(xasProData_one.EnergyPlot, XASDiffBoot[:,ii], color = 'k', alpha = 0.2, label = str(ii))
plt.xlabel('x-ray energy (eV)')
plt.ylabel('$I_{on}-I_{off}$')
plt.tight_layout()