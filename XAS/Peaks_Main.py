# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 13:48:43 2019

@author: chelsea
"""
"""
XES energy scan - k beta

"""

import numpy as np
import matplotlib.pyplot as plt
from loadData import loadData
from scipy.signal import savgol_filter
import ProcessedDataClass as PDC
import pickle
from find_t0 import find_t0_XAS

ReEnterData = False
FPlots = False
ReLoadData = False
SaveData = False
folder = "D://LCLS_Data/LCLS_python_data/XAS_Peaks/"

DorH = False #True is diode, False is HERFD

mintime = -250
maxtime = 800

NumTTStepsA = 15
NumTTStepsC = 40
NumTTStepsW = 40

if ReEnterData:

    FileNumsA = [396, 397, 399, 400, 402, 403, 405, 406, 407, 409, 410, 411, 412, 413, 414, 415, 416, 417, 419, 421]
    #FileNums = [408, 409, 410, 413, 417, 418] #[398, 401, 402, 403, 404, 405, 407]
    #FileNumsC = list(range(348, 366+1))
    #FileNumsC = list(range(348, 359+1))
    FileNumsC = list(range(350, 359+1))
    FileNumsW = list(range(342, 347+1))
    peaksRawDataA = loadData(FileNumsA, "Peaks", 1)
    peaksRawDataC = loadData(FileNumsC, "Peaks", 1)
    peaksRawDataW = loadData(FileNumsW, "Peaks", 1)


if ReLoadData:

    with open(folder + "xasPeaksData.pkl", "rb") as f:
        peaksRawData = pickle.load(f)


xasPeaksDataC = PDC.PeaksProcessedData(TTSteps = np.linspace(750,1500,NumTTStepsC+1), Delay = 1000*peaksRawDataC.TimeTool + peaksRawDataC.StageDelay*1e15)
xasPeaksDataC.makeProPeaks(peaksRawDataC, DorH, FPlots)
XASDiffPlotC = xasPeaksDataC.XASOn_Norm - xasPeaksDataC.XASOff_Norm

t0 = find_t0_XAS(xasPeaksDataC.TTSteps, XASDiffPlotC, False, True)

xasPeaksDataW = PDC.PeaksProcessedData(TTSteps = np.linspace(mintime,maxtime,NumTTStepsW+1), Delay = 1000*peaksRawDataW.TimeTool + peaksRawDataW.StageDelay*1e15 - t0)
xasPeaksDataW.makeProPeaks(peaksRawDataW, DorH, FPlots)
XASDiffPlotW = xasPeaksDataW.XASOn_Norm - xasPeaksDataW.XASOff_Norm
XASDiffErrorW = np.sqrt((np.square(xasPeaksDataW.Error_On)+np.square(xasPeaksDataW.Error_Off))/np.square(xasPeaksDataW.XASOff_Norm)+np.square(xasPeaksDataW.Error_Off)*np.square(XASDiffPlotW)/np.square(np.square(xasPeaksDataW.XASOff_Norm)))
XASDiffErrorW[np.isnan(XASDiffErrorW)] = 0
TimesW = (xasPeaksDataW.TTSteps[1:]+xasPeaksDataW.TTSteps[:-1])/2



xasPeaksDataA = PDC.PeaksProcessedData(TTSteps = np.linspace(mintime,maxtime,NumTTStepsA+1), Delay = 1000*peaksRawDataA.TimeTool + peaksRawDataA.StageDelay*1e15 - t0)
xasPeaksDataA.makeProPeaks(peaksRawDataA, DorH, FPlots)
XASDiffPlotA = xasPeaksDataA.XASOn_Norm - xasPeaksDataA.XASOff_Norm
XASDiffErrorA = np.sqrt((np.square(xasPeaksDataA.Error_On)+np.square(xasPeaksDataA.Error_Off))/np.square(xasPeaksDataA.XASOff_Norm)+np.square(xasPeaksDataA.Error_Off)*np.square(XASDiffPlotA)/np.square(np.square(xasPeaksDataA.XASOff_Norm)))
XASDiffErrorA[np.isnan(XASDiffErrorA)] = 0
TimesA = (xasPeaksDataA.TTSteps[1:]+xasPeaksDataA.TTSteps[:-1])/2



xasPeaksDataC = PDC.PeaksProcessedData(TTSteps = np.linspace(mintime,maxtime,NumTTStepsC+1), Delay = 1000*peaksRawDataC.TimeTool + peaksRawDataC.StageDelay*1e15 - t0)
xasPeaksDataC.makeProPeaks(peaksRawDataC, DorH, FPlots)
XASDiffPlotC = xasPeaksDataC.XASOn_Norm - xasPeaksDataC.XASOff_Norm
XASDiffErrorC = np.sqrt((np.square(xasPeaksDataC.Error_On)+np.square(xasPeaksDataC.Error_Off))/np.square(xasPeaksDataC.XASOff_Norm)+np.square(xasPeaksDataC.Error_Off)*np.square(XASDiffPlotC)/np.square(np.square(xasPeaksDataC.XASOff_Norm)))
XASDiffErrorC[np.isnan(XASDiffErrorC)] = 0
TimesC = (xasPeaksDataC.TTSteps[1:]+xasPeaksDataC.TTSteps[:-1])/2



fig = plt.figure()

plt.plot(TimesA, XASDiffPlotA/xasPeaksDataA.XASOff_Norm, marker='.', label = "Peak A")
plt.plot(TimesC, XASDiffPlotC/xasPeaksDataC.XASOff_Norm, marker='.', label = "Peak C")
plt.plot(TimesW, XASDiffPlotW/xasPeaksDataW.XASOff_Norm, marker='.', label = "White")

plt.xlabel('time (fs)')
plt.ylabel('change in x-ray absorption')
plt.legend()


fig = plt.figure()

plt.errorbar(TimesA, XASDiffPlotA/xasPeaksDataA.XASOff_Norm, XASDiffErrorA, marker='.', label = "Peak A")
plt.errorbar(TimesC, XASDiffPlotC/xasPeaksDataC.XASOff_Norm, XASDiffErrorC, marker='.', label = "Peak C")
plt.errorbar(TimesW, XASDiffPlotW/xasPeaksDataW.XASOff_Norm, XASDiffErrorW, marker='.', label = "White")

plt.xlabel('time (fs)')
plt.ylabel('change in x-ray absorption')
plt.legend()








if SaveData:
        
    with open(folder + "peaksRawData.pkl", "wb") as f:
        pickle.dump(peaksRawData, f)
            
    with open(folder + "xasPeaksData.pkl", "wb") as f:
        pickle.dump(xasPeaksData, f)

