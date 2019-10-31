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



APSName = h5py.File('D:\LCLS_Data\APS\APS_Aug_2015_Fesamples.mat')

indexlow = 400
indexhigh = 500



with open("D:\LCLS_Data\LCLS_python_data\XES_TimeResolved\peaksProDataPF.pkl", "rb") as f:
    peaksProDataP = pickle.load(f)


with open("D:\LCLS_Data\LCLS_python_data\XES_TimeResolved\peaksProDataMF.pkl", "rb") as f:
    peaksProDataM = pickle.load(f)
    
    
with open("D://LCLS_Data/LCLS_python_data/XES_conversion_info/x0.pkl", "rb") as f:
    x0 = pickle.load(f)

pluscolor = '#0070DF'
minuscolor = '#54A60C'


FeIII = np.array(APSName['/FeIII_ref_XES'])
FeIIISignal = FeIII[1][indexlow:indexhigh]
FeIIIEnergy = FeIII[0][indexlow:indexhigh]

FeII = np.array(APSName['/FeII_ref_XES'])
FeIISignal = FeII[1][indexlow:indexhigh]
FeIIEnergy = FeII[0][indexlow:indexhigh]


xlimL = min(FeIIEnergy*1000)
xlimH = max(FeIIEnergy*1000)

plt.figure(figsize = (4,5))

gridspec.GridSpec(10,1)

ax = plt.subplot2grid((10,1), (0,0), colspan = 1, rowspan = 3)
plt.plot(FeIIEnergy*1000, FeIISignal, color = 'k')
plt.xlim([xlimL, xlimH])
ax.set_xticklabels([])
plt.ylabel('$I_{off}$ (arb.)')
plt.tight_layout()

ax = plt.subplot2grid((10,1), (3,0), colspan = 1, rowspan = 7)
plt.plot(FeIIIEnergy*1000, (FeIIISignal-FeIISignal)/FeIISignal, color = 'k')
ax.annotate('', xy=(peaksProDataP.EnergyLabel,0.15), xytext=(peaksProDataP.EnergyLabel,-0.15), arrowprops={'arrowstyle': '->', 'ec': pluscolor, 'lw': 3})
ax.annotate('', xy=(peaksProDataM.EnergyLabel,-0.15), xytext=(peaksProDataM.EnergyLabel,0.15), arrowprops={'arrowstyle': '->', 'ec': minuscolor, 'lw': 3})
plt.xlabel('energy (eV)')
plt.ylabel('$(I_{on}-I_{off})/I_{off}$')
#plt.ylim([-4, 4])
plt.xlim([xlimL, xlimH])
plt.xticks(np.arange(6397, 6412, 4))
plt.tight_layout()










