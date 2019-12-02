# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 11:33:35 2019

@author: chelsea
"""

import scipy.io as si
import matplotlib.pyplot as plt
import numpy as np
from makeTimePlot import makeOneBootFT
import scipy.signal as ss

ScanName = si.loadmat('D:\LCLS_Data\XES\kbeta_FeRu.mat')

Fit = np.array(ScanName['Fit'])
alpha = np.array(ScanName['alpha'])
data = np.array(ScanName['data'])
delays = np.array(ScanName['delays'])
energy = np.array(ScanName['energy'])
residuals = np.array(ScanName['residuals'])

indexmax = 266
indexmin = 247

xesdiff = np.sum(data[indexmin:indexmax,:], 0)

plt.figure()
plt.pcolor(data[indexmin:indexmax,:])

plt.figure()
plt.plot(delays, xesdiff)
plt.plot(delays, ss.savgol_filter(xesdiff,5,3))

FT, Freq, X = makeOneBootFT(delays*1000, xesdiff, np.min(delays), np.max(delays), 1, 60, 30, 1, True)

plt.figure()
plt.plot(Freq, abs(FT))


indexmax = 243
indexmin = 224

xesdiff = np.sum(data[indexmin:indexmax,:], 0)

plt.figure()
plt.pcolor(data[indexmin:indexmax,:])

plt.figure()
plt.plot(delays, xesdiff)
plt.plot(delays, ss.savgol_filter(xesdiff,5,3))

FT, Freq, X = makeOneBootFT(delays*1000, xesdiff, np.min(delays), np.max(delays), 1, 60, 30, -1, True)

plt.figure()
plt.plot(Freq, abs(FT))



















#Finding the excitation population
#Run the XES_TimeScan_main and then APSXESPlot first
import math

indexP = np.where(np.round(FeIIIEnergy*1000,1)==peaksProDataP.EnergyLabel+0.1)
indexP2 = np.where(np.round(FeIIIEnergy*1000,1)==peaksProDataP2.EnergyLabel+0.1)
indexM = np.where(np.round(FeIIIEnergy*1000,1)==peaksProDataM.EnergyLabel-0.3)


StaticPercP = (FeIIISignal[indexP]-FeIISignal[indexP])/FeIISignal[indexP]
StaticPercP2 = (FeIIISignal[indexP2]-FeIISignal[indexP2])/FeIISignal[indexP2]
StaticPercM = (FeIIISignal[indexM]-FeIISignal[indexM])/FeIISignal[indexM]

StaticPerc = (StaticPercP[0]+StaticPercP2[0]-2*StaticPercM[0])/4

percentP = params[0]
percentP2 = params[5]
percentM = params[1]

covP = cov[0]
covP2 = cov[5]
covM = cov[5]



excRateP = percentP/StaticPerc*100*2
excRateP2 = percentP2/StaticPerc*100*2
excRateM = percentM/StaticPerc*100*2

excUncP = covP/StaticPerc*100*2
excUncP2 = covP2/StaticPerc*100*2
excUncM = covM/StaticPerc*100*2

print(str(round((excRateP+excRateP2-excRateM)/3,1)) + '% excitation rate $\pm$ ' + str(round((math.sqrt(excUncP**2+excUncP2**2+excUncM**2)),1)))
