# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 11:03:44 2019

@author: chelsea
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import h5py
import pickle
from makeTimePlot import makeTimePlotThreeError
from makeTimePlot import makeTimePlotSubPlot



APSName = h5py.File('D:\LCLS_Data\APS\APS_Aug_2015_Fesamples.mat')

indexlow = 400
indexhigh = 500



with open("D:\LCLS_Data\LCLS_python_data\XES_TimeResolved\peaksProDataPF.pkl", "rb") as f:
    peaksProDataP = pickle.load(f)
    
with open("D:\LCLS_Data\LCLS_python_data\XES_TimeResolved\peaksProDataP2F.pkl", "rb") as f:
    peaksProDataP2 = pickle.load(f)

with open("D:\LCLS_Data\LCLS_python_data\XES_TimeResolved\peaksProDataMF.pkl", "rb") as f:
    peaksProDataM = pickle.load(f)
    
with open("D:\LCLS_Data\LCLS_python_data\XES_TimeResolved\peaksProDataPF_boot.pkl", "rb") as f:
    peaksProDataPF_boot = pickle.load(f)
        
with open("D:\LCLS_Data\LCLS_python_data\XES_TimeResolved\peaksProDataMF_boot.pkl", "rb") as f:
    peaksProDataMF_boot = pickle.load(f)
    
with open("D:\LCLS_Data\LCLS_python_data\XES_TimeResolved\peaksProDataP2F_boot.pkl", "rb") as f:
    peaksProDataP2F_boot = pickle.load(f)

with open("D:\LCLS_Data\LCLS_python_data\XES_TimeResolved\TCentersPF.pkl", "rb") as f:
    TCentersPF = pickle.load(f)

with open("D:\LCLS_Data\LCLS_python_data\XES_TimeResolved\TCentersP2F.pkl", "rb") as f:
    TCentersP2F = pickle.load(f)

with open("D:\LCLS_Data\LCLS_python_data\XES_TimeResolved\TCentersMF.pkl", "rb") as f:
    TCentersMF = pickle.load(f)
        
with open("D://LCLS_Data/LCLS_python_data/XES_conversion_info/x0.pkl", "rb") as f:
    x0 = pickle.load(f)
    


pluscolor = '#009E73'
minuscolor = '#0072b2'
pluscolor2 = '#e69f00'


FeIII = np.array(APSName['/FeIII_ref_XES'])
FeIIISignal = FeIII[1][indexlow:indexhigh]
FeIIIEnergy = FeIII[0][indexlow:indexhigh]

FeII = np.array(APSName['/FeII_ref_XES'])
FeIISignal = FeII[1][indexlow:indexhigh]
FeIIEnergy = FeII[0][indexlow:indexhigh]


xlimL = min(FeIIEnergy*1000)
xlimH = max(FeIIEnergy*1000)

MinTimePlots = -250
MaxTimePlots = 1400

FPlots = False

#makeTimePlotThreeError(TCentersPF, TCentersP2F, TCentersMF, peaksProDataPF_boot, peaksProDataP2F_boot, peaksProDataMF_boot, MinTimePlots, MaxTimePlots, 0, FPlots, True)
makeTimePlotSubPlot(FeIIIEnergy, FeIIISignal, FeIIEnergy, FeIISignal, TCentersPF, TCentersP2F, TCentersMF, peaksProDataPF_boot, peaksProDataP2F_boot, peaksProDataMF_boot, MinTimePlots, MaxTimePlots, 0, FPlots, True)

plt.figure(figsize = (4,5))

gridspec.GridSpec(10,1)

ax = plt.subplot2grid((10,1), (0,0), colspan = 1, rowspan = 3)
plt.plot(FeIIEnergy*1000, FeIISignal, color = 'k', label = 'FeII')
plt.plot(FeIIIEnergy*1000, FeIIISignal, color = 'k', linestyle='--', label = 'FeIII')
plt.xlim([xlimL, xlimH])
plt.xticks(np.arange(6397, 6412, 4))
ax.set_xticklabels([])
plt.ylabel('emission')
plt.legend()
plt.tight_layout()

ax = plt.subplot2grid((10,1), (3,0), colspan = 1, rowspan = 7)
plt.plot(FeIIIEnergy*1000, (FeIIISignal-FeIISignal)/FeIISignal, color = 'k')
ax.annotate('', xy=(peaksProDataP.EnergyLabel,0.2), xytext=(peaksProDataP.EnergyLabel,-0.13), arrowprops={'arrowstyle': '->', 'ls': 'dotted', 'ec': pluscolor, 'lw': 3})
ax.annotate('', xy=(peaksProDataM.EnergyLabel,-0.13), xytext=(peaksProDataM.EnergyLabel,0.2), arrowprops={'arrowstyle': '->', 'ls': 'dashed', 'ec': minuscolor, 'lw': 3})
ax.annotate('', xy=(peaksProDataP2.EnergyLabel,0.2), xytext=(peaksProDataP2.EnergyLabel,-0.13), arrowprops={'arrowstyle': '->', 'ec': pluscolor2, 'lw': 3})
plt.xlabel('energy (eV)')
plt.ylabel('rel. $\Delta$ emission')
#plt.ylim([-4, 4])
plt.xlim([xlimL, xlimH])
plt.xticks(np.arange(6397, 6412, 4))
plt.tight_layout()








