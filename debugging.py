# -*- coding: utf-8 -*-
"""
Created on Tue May  7 13:10:47 2019

@author: chelsea
"""

from find_t0_XAS import find_t0_XAS

t0 = find_t0_XAS(XOn, LOn, XEnergyRaw, TimeTool, Ipm2Sum, RowlandY, Filter, True)

for ii in range(NumEnergySteps):
    if On_NumScan[0][ii] > 0:
        error[ii] = XASDiffPlot[0][ii]/math.sqrt(On_NumScan[0][ii])
        
plt.figure(), plt.errorbar(EnergyPlot, XASDiffPlot[0], error)