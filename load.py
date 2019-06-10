# -*- coding: utf-8 -*-
"""
Created on Thu May 16 10:31:17 2019

@author: chelsea
"""
import pickle

folder = "D://LCLS_Data/LCLS_python_data/XAS/"

with open(folder + "XOn.pkl", "rb") as f:
    XOn = pickle.load(f)
    
with open(folder + "LOn.pkl", "rb") as f:
    LOn = pickle.load(f)
    
try:
    with open(folder + "XEnergyRaw.pkl", "rb") as f:
        XEnergyRaw = pickle.load(f)
except:
    print('no XEnergyRaw variable')
    
try:
    with open(folder + "StageDelay.pkl", "wb") as f:
        StageDelay = pickle.load(f)
except:
    print('no StageDelay variable')
    
with open(folder + "Diode2.pkl", "rb") as f:
    Diode2 = pickle.load(f)
    
with open(folder + "Ipm2Sum.pkl", "rb") as f:
    Ipm2Sum = pickle.load(f)

with open(folder + "Ipm2Median.pkl", "rb") as f:
    Ipm2Median = pickle.load(f)
    
with open(folder + "Ipm2STD.pkl", "rb") as f:
    Ipm2STD = pickle.load(f)
    
with open(folder + "DiodeIpmSlope.pkl", "rb") as f:
    DiodeIpmSlope = pickle.load(f)
    
with open(folder + "DISMedian.pkl", "rb") as f:
    DISMedian = pickle.load(f)
    
with open(folder + "DISSTD.pkl", "rb") as f:
    DISSTD = pickle.load(f)
    
with open(folder + "TimeTool.pkl", "rb") as f:
    TimeTool = pickle.load(f)
    
with open(folder + "TTMedian.pkl", "rb") as f:
    TTMedian = pickle.load(f)
    
with open(folder + "TTSTD.pkl", "rb") as f:
    TTSTD = pickle.load(f)
    
with open(folder + "TTAmp.pkl", "rb") as f:
    TTAmp = pickle.load(f)

with open(folder + "TTAmpMedian.pkl", "rb") as f:
    TTAmpMedian = pickle.load(f)

with open(folder + "TTAmpSTD.pkl", "rb") as f:
    TTAmpSTD = pickle.load(f)

with open(folder + "TTFWHM.pkl", "rb") as f:
    TTFWHM = pickle.load(f)
    
with open(folder + "TTFWHMMedian.pkl", "rb") as f:
    TTFWHMMedian = pickle.load(f)
    
with open(folder + "TTFWHMSTD.pkl", "rb") as f:
    TTFWHMSTD = pickle.load(f)
    
with open(folder + "ScanNum.pkl", "rb") as f:
    ScanNum = pickle.load(f)
    
with open(folder + "RowlandY.pkl", "rb") as f:
    RowlandY = pickle.load(f)