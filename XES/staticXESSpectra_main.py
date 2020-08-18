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
import matplotlib.pyplot as plt
from MakeRawBoot import MakeRawBootXES
import time
import datetime

folder = "D://LCLS_Data/LCLS_python_data/XES_Spectra/"
ReEnterData = True
FPlots = False
ReLoadData = False
SaveData = True

MinTime = -100
MaxTime = 100


if ReEnterData:

    FileNums = list(range(190,190+1))
    xesRawData = loadData(FileNums, "XES", 2)

if ReLoadData:

    with open(folder + "xesRawData.pkl", "rb") as f:
        xesRawData = pickle.load(f)



confolder = "D://LCLS_Data/LCLS_python_data/XES_conversion_info/"
exists = os.path.isfile(confolder + "t0.pkl")

if exists:
    with open(confolder + "t0.pkl", "rb") as f:
        t0 = pickle.load(f)
        
    xesProData = PDC.XESProcessedData(TTDelay = 1000*xesRawData.TimeTool - 1400 - t0)

    print('read in t0')
else:
    xesProData = PDC.XESProcessedData(TTDelay = 1000*xesRawData.TimeTool)




xesProData.changeValue(UniAngle = np.unique(xesRawData.Angle))
xesProData.changeValue(RowWOffset = xesRawData.RowlandY - xesRawData.Offset)

xesProData.makeProXES(xesRawData, MaxTime, MinTime, FPlots)
xesProData.energyConversion(True)


numboot = 1000
startT = time.time()

for ii in range(numboot):
    
    xesRawBoot = MakeRawBootXES(xesRawData)
        
    xesProData_loop = PDC.XESProcessedData(TTDelay = 1000*xesRawBoot.TimeTool - 1400 - t0, \
                                           UniAngle = np.unique(xesRawBoot.Angle), RowWOffset = xesRawBoot.RowlandY - xesRawBoot.Offset)
    xesProData_loop.makeProXES(xesRawBoot, MaxTime, MinTime, FPlots)
    xesProData_loop.getEnergy()
    
    if ii == 0:
        
        xesProData_boot = xesProData_loop
        xesProData_boot.changeValue(Num_Boot = np.ones(np.shape(xesProData_boot.UniAngle)))
        
    else:
        
        xesProData_boot.add(xesProData_loop)

    elapsed = time.time() - startT
    timeleft = elapsed/(ii+1)*(numboot-ii-1)
    print('time left ' + str(datetime.timedelta(seconds = timeleft)) + ' seconds')
        

xesProData_boot.boot_ave()


xesProData_boot.makeStaticPlot()




if SaveData:
        
    with open(folder + "xesRawData.pkl", "wb") as f:
        pickle.dump(xesRawData, f)
            
    with open(folder + "xesProData.pkl", "wb") as f:
        pickle.dump(xesProData_boot, f)











