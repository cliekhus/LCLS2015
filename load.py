# -*- coding: utf-8 -*-
"""
Created on Thu May 16 10:31:17 2019

@author: chelsea
"""
import pickle

with open("D://LCLS_Data/LCLS_python_data/XOn.pkl", "rb") as f:
    XOn = pickle.load(f)
    
with open("D://LCLS_Data/LCLS_python_data/LOn.pkl", "rb") as f:
    LOn = pickle.load(f)
    
try:
    with open("D://LCLS_Data/LCLS_python_data/XEnergyRaw.pkl", "rb") as f:
        pickle.load(f)
except:
    print('no XEnergyRaw variable')
    
try:
    with open("D://LCLS_Data/LCLS_python_data/StageDelay.pkl", "wb") as f:
        pickle.load(f)
except:
    print('no StageDelay variable')
    
with open("D://LCLS_Data/LCLS_python_data/Diode2.pkl", "rb") as f:
    Diode2 = pickle.load(f)
    
with open("D://LCLS_Data/LCLS_python_data/Ipm2Sum.pkl", "rb") as f:
    Ipm2Sum = pickle.load(f)

with open("D://LCLS_Data/LCLS_python_data/Ipm2Median.pkl", "rb") as f:
    Ipm2Median = pickle.load(f)
    
with open("D://LCLS_Data/LCLS_python_data/Ipm2STD.pkl", "rb") as f:
    Ipm2STD = pickle.load(f)
    
with open("D://LCLS_Data/LCLS_python_data/DiodeIpmSlope.pkl", "rb") as f:
    DiodeIpmSlope = pickle.load(f)
    
with open("D://LCLS_Data/LCLS_python_data/DISMedian.pkl", "rb") as f:
    DISMedian = pickle.load(f)
    
with open("D://LCLS_Data/LCLS_python_data/DISSTD.pkl", "rb") as f:
    DISSTD = pickle.load(f)
    
with open("D://LCLS_Data/LCLS_python_data/TimeTool.pkl", "rb") as f:
    TimeTool = pickle.load(f)
    
with open("D://LCLS_Data/LCLS_python_data/TTMedian.pkl", "rb") as f:
    TTMedian = pickle.load(f)
    
with open("D://LCLS_Data/LCLS_python_data/TTSTD.pkl", "rb") as f:
    TTSTD = pickle.load(f)
    
with open("D://LCLS_Data/LCLS_python_data/TTAmp.pkl", "rb") as f:
    TTAmp = pickle.load(f)

with open("D://LCLS_Data/LCLS_python_data/TTAmpMedian.pkl", "rb") as f:
    TTAmpMedian = pickle.load(f)

with open("D://LCLS_Data/LCLS_python_data/TTAmpSTD.pkl", "rb") as f:
    TTAmpSTD = pickle.load(f)

with open("D://LCLS_Data/LCLS_python_data/TTFWHM.pkl", "rb") as f:
    TTFWHM = pickle.load(f)
    
with open("D://LCLS_Data/LCLS_python_data/TTFWHMMedian.pkl", "rb") as f:
    TTFWHMMedian = pickle.load(f)
    
with open("D://LCLS_Data/LCLS_python_data/TTFWHMSTD.pkl", "rb") as f:
    TTFWHMSTD = pickle.load(f)
    
with open("D://LCLS_Data/LCLS_python_data/ScanNum.pkl", "rb") as f:
    ScanNum = pickle.load(f)
    
with open("D://LCLS_Data/LCLS_python_data/RowlandY.pkl", "rb") as f:
    RowlandY = pickle.load(f)