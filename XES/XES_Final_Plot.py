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
from makeTimePlot import makeTimePlotSubPlot_LCLS
from scipy.signal import savgol_filter



APSName = h5py.File('C:\LCLS_Data\APS\APS_Aug_2015_Fesamples.mat')

indexlow = 400
indexhigh = 500



with open("C:\LCLS_Data\LCLS_python_data\XES_TimeResolved\peaksProDataPF.pkl", "rb") as f:
    peaksProDataP = pickle.load(f)
    
with open("C:\LCLS_Data\LCLS_python_data\XES_TimeResolved\peaksProDataP2F.pkl", "rb") as f:
    peaksProDataP2 = pickle.load(f)

with open("C:\LCLS_Data\LCLS_python_data\XES_TimeResolved\peaksProDataMF.pkl", "rb") as f:
    peaksProDataM = pickle.load(f)
    
with open("C:\LCLS_Data\LCLS_python_data\XES_TimeResolved\peaksProDataPF_boot.pkl", "rb") as f:
    peaksProDataPF_boot = pickle.load(f)
        
with open("C:\LCLS_Data\LCLS_python_data\XES_TimeResolved\peaksProDataMF_boot.pkl", "rb") as f:
    peaksProDataMF_boot = pickle.load(f)
    
with open("C:\LCLS_Data\LCLS_python_data\XES_TimeResolved\peaksProDataP2F_boot.pkl", "rb") as f:
    peaksProDataP2F_boot = pickle.load(f)

with open("C:\LCLS_Data\LCLS_python_data\XES_TimeResolved\TCentersPF.pkl", "rb") as f:
    TCentersPF = pickle.load(f)

with open("C:\LCLS_Data\LCLS_python_data\XES_TimeResolved\TCentersP2F.pkl", "rb") as f:
    TCentersP2F = pickle.load(f)

with open("C:\LCLS_Data\LCLS_python_data\XES_TimeResolved\TCentersMF.pkl", "rb") as f:
    TCentersMF = pickle.load(f)
        
with open("C://LCLS_Data/LCLS_python_data/XES_conversion_info/x0.pkl", "rb") as f:
    x0 = pickle.load(f)

with open("C://LCLS_Data/LCLS_python_data/XES_Spectra/xesProData.pkl", "rb") as f:
    static = pickle.load(f)


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

#makeTimePlotSubPlot(FeIIIEnergy, FeIIISignal, FeIIEnergy, FeIISignal, TCentersPF, TCentersP2F, TCentersMF, peaksProDataPF_boot, peaksProDataP2F_boot, peaksProDataMF_boot, MinTimePlots, MaxTimePlots, 0, FPlots, True)

StaticS = savgol_filter((static.XESOn_Norm - static.XESOff_Norm)/static.XESOff_Norm*100, 5,3)
StaticEr = np.sqrt(static.Error_On**2+static.Error_On**2)/static.XESOff_Norm*100

#makeTimePlotSubPlot_LCLS(FeIIEnergy, FeIISignal, static.KaEnergy, StaticS, StaticEr, TCentersPF, TCentersP2F, TCentersMF, peaksProDataPF_boot, peaksProDataP2F_boot, peaksProDataMF_boot, MinTimePlots, MaxTimePlots, 0, FPlots, True)
makeTimePlotSubPlot_LCLS(static.KaEnergy, static.XESOff_Norm/np.max(static.XESOff_Norm), static.KaEnergy, StaticS, StaticEr, TCentersPF, TCentersP2F, TCentersMF, peaksProDataPF_boot, peaksProDataP2F_boot, peaksProDataMF_boot, MinTimePlots, MaxTimePlots, 0, FPlots, True)


plt.figure(figsize = (3.33,5))

gridspec.GridSpec(10,1)

ax = plt.subplot2grid((10,1), (0,0), colspan = 1, rowspan = 3)
plt.plot(FeIIEnergy*1000, FeIISignal/max(FeIISignal), color = 'k', label = 'FeII')
plt.plot(FeIIIEnergy*1000, FeIIISignal/max(FeIISignal), color = 'k', linestyle='--', label = 'FeIII')
plt.xlim([xlimL, xlimH])
plt.xticks(np.arange(6397, 6412, 4))
ax.set_xticklabels([])
plt.ylabel('emission')
plt.legend()
plt.tight_layout()

ax = plt.subplot2grid((10,1), (3,0), colspan = 1, rowspan = 7)
plt.plot(FeIIIEnergy*1000, (FeIIISignal-FeIISignal)/FeIISignal*100, color = 'k')
#plt.plot(FeIIIEnergy*1000, (FeIIISignal-FeIISignal), color = 'k')
ax.annotate('', xy=(peaksProDataP.EnergyLabel,0.2*100), xytext=(peaksProDataP.EnergyLabel,-0.13*100), arrowprops={'arrowstyle': '->', 'ls': 'dotted', 'ec': pluscolor, 'lw': 3})
ax.annotate('', xy=(peaksProDataM.EnergyLabel,-0.13*100), xytext=(peaksProDataM.EnergyLabel,0.2*100), arrowprops={'arrowstyle': '->', 'ls': 'dashed', 'ec': minuscolor, 'lw': 3})
ax.annotate('', xy=(peaksProDataP2.EnergyLabel,0.2*100), xytext=(peaksProDataP2.EnergyLabel,-0.13*100), arrowprops={'arrowstyle': '->', 'ec': pluscolor2, 'lw': 3})
plt.xlabel('energy (eV)')
plt.ylabel('% $\Delta$ emission')
#plt.ylim([-4, 4])
plt.xlim([xlimL, xlimH])
plt.xticks(np.arange(6397, 6412, 4))
plt.tight_layout()








