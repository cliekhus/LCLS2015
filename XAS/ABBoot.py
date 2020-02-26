# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 14:18:42 2020

@author: chelsea
"""


import pickle
from fitXASDiff import fitXASPiecewiseGauss
from fittingfunctions import gauswslope
import numpy as np
import matplotlib.pyplot as plt



folder = "D://LCLS_Data/LCLS_python_data/XAS_Spectra/"

with open(folder + "XASDiffBoot.pkl", "rb") as f:
    XASDiffBoot = pickle.load(f)
    
with open(folder + "XASDiffBootF.pkl", "rb") as f:
    XASDiffBootF = pickle.load(f)
    
with open(folder + "XASDiffBootE.pkl", "rb") as f:
    XASDiffBootE = pickle.load(f)
    
with open(folder + "XASOffBootF.pkl", "rb") as f:
    XASOffBootF = pickle.load(f)
    
with open(folder + "XASOffBootE.pkl", "rb") as f:
    XASOffBootE = pickle.load(f)

with open(folder + "XASOnBootF.pkl", "rb") as f:
    XASOnBootF = pickle.load(f)
        
with open(folder + "xasProData_one.pkl", "rb") as f:
    xasProData_one = pickle.load(f)
    
    



numboot = 1000

Asig = np.empty(numboot)
Bsig = np.empty(numboot)

Ax0 = np.empty(numboot)
Bx0 = np.empty(numboot)

Aa = np.empty(numboot)
Ba = np.empty(numboot)

Aoff = np.empty(numboot)
Boff = np.empty(numboot)

Aslope = np.empty(numboot)
Bslope = np.empty(numboot)

errorhit = 0


for ii in range(numboot):
    
    try:
            
        Fit,Params,ParamsA,ParamsB,covA,covB = \
            fitXASPiecewiseGauss(xasProData_one.EnergyPlot, XASDiffBoot[:,ii], XASOffBootF, XASOnBootF, False)
    except:
        
        errorhit += 1


    Asig[ii-errorhit] = ParamsA[0]
    Bsig[ii-errorhit] = ParamsB[0]

    Ax0[ii-errorhit] = ParamsA[1]
    Bx0[ii-errorhit] = ParamsB[1]
    
    Aa[ii-errorhit] = ParamsA[2]
    Ba[ii-errorhit] = ParamsB[2]
    
    Aoff[ii-errorhit] = ParamsA[3]
    Boff[ii-errorhit] = ParamsB[3]
    
    Aslope[ii-errorhit] = ParamsA[4]
    Bslope[ii-errorhit] = ParamsB[4]
    
Asig = Asig[:numboot-errorhit]
Bsig = Bsig[:numboot-errorhit]

Ax0 = Ax0[:numboot-errorhit]
Bx0 = Bx0[:numboot-errorhit]

Aa = Aa[:numboot-errorhit]
Ba = Ba[:numboot-errorhit]

Aoff = Aoff[:numboot-errorhit]
Boff = Boff[:numboot-errorhit]

Aslope = Aslope[:numboot-errorhit]
Bslope = Bslope[:numboot-errorhit]

cond = np.logical_and.reduce((Ax0>7110, Bx0<7115, Ax0<7113))

fitout = {'Asig': np.mean(Asig[cond]), 'Bsig': np.mean(Bsig[cond]), \
          'Ax0': np.mean(Ax0[cond]), 'Bx0': np.mean(Bx0[cond]), \
          'Ax0unc': np.std(Ax0[cond]), 'Bx0unc': np.std(Bx0[cond]), \
          'BmA': np.mean(Bx0[cond]-Ax0[cond]), 'BmAunc': np.std(Bx0[cond]-Ax0[cond]), \
          'Aa': np.mean(Ax0[cond]), 'Ba': np.mean(Bx0[cond]), \
          'Aoff': np.mean(Ax0[cond]), 'Boff': np.mean(Bx0[cond]), \
          'Aslope': np.mean(Ax0[cond]), 'Bslope': np.mean(Bx0[cond])}



with open(folder + "FitOuts.pkl", "wb") as f:
    XASDiffBoot = pickle.dump(fitout, f)









    