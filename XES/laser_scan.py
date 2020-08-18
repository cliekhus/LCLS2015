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
import matplotlib.pyplot as plt

folder = "D://LCLS_Data/LCLS_python_data/XES_Spectra/"
ReEnterData = True
FPlots = False
ReLoadData = False
SaveData = False

MinTime = -30
MaxTime = 30


if ReEnterData:

    FileNums = [106]
    xesRawData = loadData(FileNums, "XES", 2)

if ReLoadData:

    with open(folder + "xesRawData.pkl", "rb") as f:
        xesRawData = pickle.load(f)



confolder = "D://LCLS_Data/LCLS_python_data/XES_conversion_info/"
exists = os.path.isfile(confolder + "t0.pkl")

if exists:
    with open(confolder + "t0.pkl", "rb") as f:
        t0 = pickle.load(f)
        
    xesProData = PDC.XESProcessedData(TTDelay = 1000*xesRawData.TimeTool - 1500 - t0)

    print('read in t0')
else:
    xesProData = PDC.XESProcessedData(TTDelay = 1000*xesRawData.TimeTool)

#xesProData = PDC.XESProcessedData(TTDelay = 1000*xesRawData.TimeTool)

xesProData.changeValue(UniAngle = np.unique(xesRawData.Angle))
#xesProData.changeValue(RowWOffset = xesRawData.RowlandY - xesRawData.Offset)
xesProData.changeValue(RowWOffset = xesRawData.RowlandY)

xesProData.makeLaserXES(xesRawData, MaxTime, MinTime, FPlots)
#xesProData.energyConversion(True)



UA = 75.445
import pickle

folder = "D://LCLS_Data/LCLS_python_data/XES_conversion_info/"

with open(folder + "slope.pkl", "rb") as f:
    slope = pickle.load(f)
    
with open(folder + "x0.pkl", "rb") as f:
    x0 = pickle.load(f)
    
LCLSEnergy = -UA*slope+x0



plt.figure(figsize = (4,5))
plt.plot(xesProData.UniAngle, (xesProData.XESOn_Norm-xesProData.XESOff_Norm)/xesProData.XESOff_Norm*100, label = str(int(LCLSEnergy*1000)) + ' eV')
plt.xlabel('laser energy ($\mu$J)')
plt.ylabel('%$\Delta$ emission')
plt.tight_layout()

m,b = np.polyfit(xesProData.UniAngle, (xesProData.XESOn_Norm-xesProData.XESOff_Norm)/xesProData.XESOff_Norm*100,1)
x_new = np.linspace(np.min(xesProData.UniAngle), np.max(xesProData.UniAngle), 100)
y_new = m*x_new+b
plt.plot(x_new, y_new, label = 'linear fit')




plt.legend()