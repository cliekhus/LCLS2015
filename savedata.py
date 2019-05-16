# -*- coding: utf-8 -*-
"""
Created on Thu May 16 10:22:18 2019

@author: chelsea
"""
import pickle

with open("D://LCLS_Data/LCLS_python_data/XOn.pkl", "wb") as f:
    pickle.dump(XOn, f)
    
with open("D://LCLS_Data/LCLS_python_data/LOn.pkl", "wb") as f:
    pickle.dump(LOn, f)
    
with open("D://LCLS_Data/LCLS_python_data/XEnergyRaw.pkl", "wb") as f:
    pickle.dump(XEnergyRaw, f)
    
with open("D://LCLS_Data/LCLS_python_data/Diode2.pkl", "wb") as f:
    pickle.dump(Diode2, f)
    
with open("D://LCLS_Data/LCLS_python_data/Ipm2Sum.pkl", "wb") as f:
    pickle.dump(Ipm2Sum, f)

with open("D://LCLS_Data/LCLS_python_data/Ipm2Median.pkl", "wb") as f:
    pickle.dump(Ipm2Median, f)
    
with open("D://LCLS_Data/LCLS_python_data/Ipm2STD.pkl", "wb") as f:
    pickle.dump(Ipm2STD, f)

with open("D://LCLS_Data/LCLS_python_data/DiodeIpmSlope.pkl", "wb") as f:
    pickle.dump(DiodeIpmSlope, f)
    
with open("D://LCLS_Data/LCLS_python_data/DISMedian.pkl", "wb") as f:
    pickle.dump(DISMedian, f)
    
with open("D://LCLS_Data/LCLS_python_data/DISSTD.pkl", "wb") as f:
    pickle.dump(DISSTD, f)
    
with open("D://LCLS_Data/LCLS_python_data/TimeTool.pkl", "wb") as f:
    pickle.dump(TimeTool, f)
    
with open("D://LCLS_Data/LCLS_python_data/TTMedian.pkl", "wb") as f:
    pickle.dump(TTMedian, f)
    
with open("D://LCLS_Data/LCLS_python_data/TTSTD.pkl", "wb") as f:
    pickle.dump(TTSTD, f)
    
with open("D://LCLS_Data/LCLS_python_data/TTAmp.pkl", "wb") as f:
    pickle.dump(TTAmp, f)

with open("D://LCLS_Data/LCLS_python_data/TTAmpMedian.pkl", "wb") as f:
    pickle.dump(TTAmpMedian, f)

with open("D://LCLS_Data/LCLS_python_data/TTAmpSTD.pkl", "wb") as f:
    pickle.dump(TTAmpSTD, f)

with open("D://LCLS_Data/LCLS_python_data/TTFWHM.pkl", "wb") as f:
    pickle.dump(TTFWHM, f)
    
with open("D://LCLS_Data/LCLS_python_data/TTFWHMMedian.pkl", "wb") as f:
    pickle.dump(TTFWHMMedian, f)
    
with open("D://LCLS_Data/LCLS_python_data/TTFWHMSTD.pkl", "wb") as f:
    pickle.dump(TTFWHMSTD, f)
    
with open("D://LCLS_Data/LCLS_python_data/ScanNum.pkl", "wb") as f:
    pickle.dump(ScanNum, f)
    
with open("D://LCLS_Data/LCLS_python_data/RowlandY.pkl", "wb") as f:
    pickle.dump(RowlandY, f)

#XOn, LOn, XEnergyRaw, Diode2, Ipm2Sum, Ipm2Median, Ipm2STD, DiodeIpmSlope, DISMedian, DISSTD, TimeTool, TTMedian, TTSTD, TTAmp, TTAmpMedian, TTAmpSTD, TTFWHM, TTFWHMMedian, TTFWHMSTD, ScanNum, RowlandY