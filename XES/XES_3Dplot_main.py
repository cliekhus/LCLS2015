# -*- coding: utf-8 -*-
"""
Created on Mon May 20 10:34:43 2019

@author: chelsea
"""


from APSXESCalibration import convertAngle2Energy
from XES_TimeScan_fn import XES_TimeScan_fn


folder = "D://LCLS_Data/LCLS_python_data/XES_TimeResolved/"
ReEnterData = True
FPlots = False
ReLoadData = True
SaveData = False
Boot = True

NumTTSteps = 100
NumTTStepsPlots = 50

MinTimePlots = -250
MaxTimePlots = 1400

FileNums = [list(range(180,188+1))]
FileNums.append(list(range(131,140+1)))
FileNums.append(list(range(165,178+1)))
FileNums.append(list(range(144, 154+1)))
FileNums.append(list(range(123, 130+1)))
FileNums.append(list(range(155,164+1)))


starta = [0.02, 0.009, 0.02, 0.02, 0.02, 0.02]
startrate = [59, 60, 60, 60, 60, 60]
startsig = [6, 6, 8, 6, 6, 6]
PorM = [True, True, False, False, True, True]

for ii in range(len(FileNums)):

    
    if ii == 0:
        PeaksBootF, PeaksBootE, FTBootF, FTBootE, Freq, TCenters = XES_TimeScan_fn(FileNums[ii], PorM[ii], ReEnterData, SaveData, ReLoadData, starta[ii], startrate[ii], startsig[ii], False)
        
        PeaksBootF = [PeaksBootF]
        PeaksBootE = [PeaksBootE]
        FTBootF = [FTBootF]
        FTBootE = [FTBootE]
        Freq = [Freq]
        TCenters = [TCenters]
        Energy = [convertAngle2Energy(FileNums[ii][0], True)]
        
    else:
        peaksBootF, peaksBootE, ftBootF, ftBootE, freq, tCenters = XES_TimeScan_fn(FileNums[ii], PorM[ii], ReEnterData, SaveData, ReLoadData, starta[ii], startrate[ii], startsig[ii], False)

        PeaksBootF.append(peaksBootF)
        PeaksBootE.append(peaksBootE)
        FTBootF.append(ftBootF)
        FTBootE.append(ftBootE)
        Freq.append(freq)
        TCenters.append(tCenters)
        Energy = Energy + [convertAngle2Energy(FileNums[ii][0], True)]
