# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 11:03:44 2019

@author: chelsea
"""

import numpy as np
from loadData import loadData
import os
import pickle
import ProcessedDataClass as PDC

folder = "D://LCLS_Data/LCLS_python_data/XES_Spectra/"
ReEnterData = True
FPlots = False
ReLoadData = False
SaveData = True

MinTime = -25
MaxTime = 25


if ReEnterData:

    FileNums = list(range(190,190+1))
    xesRawData = loadData(FileNums, "XES", 2)

if ReLoadData:

    with open(folder + "xesRawData.pkl", "rb") as f:
        xesRawData = pickle.load(f)



exists = os.path.isfile("D://LCLS_Data/LCLS_python_data/XES_conversion_info/t0.pkl")

if exists:
    with open(folder + "t0.pkl", "rb") as f:
        t0 = pickle.load(f)
        
    xesProData = PDC.XESProcessedData(TTDelay = 1000*xesRawData.TimeTool - 1400 - t0)

    print('read in t0')
else:
    xesProData = PDC.XESProcessedData(TTDelay = 1000*xesRawData.TimeTool)




xesProData.changeValue(UniAngle = np.unique(xesRawData.Angle))
xesProData.changeValue(RowWOffset = xesRawData.RowlandY - xesRawData.Offset)

xesProData.makeProXES(xesRawData, MaxTime, MinTime, FPlots)
xesProData.energyConversion(FPlots)

xesProData.makeStaticPlot()




if SaveData:
        
    with open(folder + "xesRawData.pkl", "wb") as f:
        pickle.dump(xesRawData, f)
            
    with open(folder + "xesProData.pkl", "wb") as f:
        pickle.dump(xesProData, f)











