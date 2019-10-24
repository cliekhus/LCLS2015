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


ReEnterData = False
FPlots = False

MinTime = -25
MaxTime = 25


if ReEnterData:

    FileNums = list(range(190,190+1))
    xesRawData = loadData(FileNums, "XES", 2)

folder = "D://LCLS_Data/LCLS_python_data/XES_conversion_info/"
exists = os.path.isfile(folder+'t0.pkl')



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















